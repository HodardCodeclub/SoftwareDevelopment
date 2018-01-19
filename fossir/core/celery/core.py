# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import logging
import os
from datetime import datetime
from operator import itemgetter

from celery import Celery
from celery.app.log import Logging
from celery.beat import PersistentScheduler
from celery.schedules import BaseSchedule
from contextlib2 import ExitStack
from flask_pluginengine import current_plugin, plugin_context
from pytz import timezone
from sqlalchemy import inspect
from terminaltables import AsciiTable

from fossir.core.celery.util import locked_task
from fossir.core.config import config
from fossir.core.db import db
from fossir.core.notifications import flush_email_queue, init_email_queue
from fossir.core.plugins import plugin_engine
from fossir.util.console import cformat
from fossir.util.fossilize import clearCache
from fossir.util.string import return_ascii
from fossir.web.flask.stats import request_stats_request_started


class fossirCelery(Celery):
    """Celery sweetened with some fossir/Flask-related sugar

    The following extra params are available on the `task` decorator:

    - `request_context` -- if True, the task will run inside a Flask
                           `test_request_context`
    - `plugin` -- if set to a plugin name or class, the task will run
                  inside a plugin context for that plugin.  This will
                  override whatever plugin context is active when
                  sending the task.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log', fossirCeleryLogging)
        super(fossirCelery, self).__init__(*args, **kwargs)
        self.flask_app = None
        self._patch_task()
        # XXX: needed to keep using localtime-based crontab schedules
        # without having the broken timezone handling in celery 4.1
        # TODO: once a new celery version is out, revert the commit that
        # adds this hack, sets `nowfun` and comments out the timezone
        # config option.
        BaseSchedule.now = lambda self: datetime.now(timezone(config.DEFAULT_TIMEZONE))

    def init_app(self, app):
        if not config.CELERY_BROKER and not app.config['TESTING']:
            raise ValueError('Celery broker URL is not set')
        self.conf['broker_url'] = config.CELERY_BROKER
        self.conf['result_backend'] = config.CELERY_RESULT_BACKEND or config.CELERY_BROKER
        self.conf['beat_scheduler'] = fossirPersistentScheduler
        self.conf['beat_schedule_filename'] = os.path.join(config.TEMP_DIR, 'celerybeat-schedule')
        self.conf['worker_hijack_root_logger'] = False
        # self.conf['timezone'] = config.DEFAULT_TIMEZONE  # XXX: broken in celery 4.1
        self.conf['task_ignore_result'] = True
        self.conf['task_store_errors_even_if_ignored'] = True
        self.conf['worker_redirect_stdouts'] = not app.debug
        # Pickle isn't pretty but that way we can pass along all types (tz-aware datetimes, sets, etc.)
        self.conf['result_serializer'] = 'pickle'
        self.conf['task_serializer'] = 'pickle'
        self.conf['accept_content'] = ['json', 'yaml', 'pickle']
        # Allow fossir.conf to override settings
        self.conf.update(config.CELERY_CONFIG)
        assert self.flask_app is None or self.flask_app is app
        self.flask_app = app

    def periodic_task(self, *args, **kwargs):
        """Decorator to register a periodic task.

        This behaves like the :meth:`task` decorator, but automatically
        schedules the task to execute periodically, using extra kwargs
        as described in the Celery documentation:
        http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html#available-fields

        :param locked: Set this to ``False`` if you want to allow the
                       task to run more than once at the same time.
        """
        def decorator(f):
            if kwargs.pop('locked', True):
                f = locked_task(f)
            entry = {
                'schedule': kwargs.pop('run_every'),
                'args': kwargs.pop('args', ()),
                'kwargs': kwargs.pop('kwargs', {}),
                'options': kwargs.pop('options', {}),
                'relative': kwargs.pop('relative', False)
            }
            kwargs.setdefault('ignore_result', True)
            task = self.task(f, *args, **kwargs)
            entry['task'] = task.name
            self.conf['beat_schedule'][task.name] = entry
            return task

        return decorator

    def _patch_task(self):
        """Patches the `task` decorator to run tasks inside the fossir environment"""
        class fossirTask(self.Task):
            abstract = True

            def apply_async(s, args=None, kwargs=None, task_id=None, producer=None,
                            link=None, link_error=None, shadow=None, **options):
                if args is not None:
                    args = _CelerySAWrapper.wrap_args(args)
                if kwargs is not None:
                    kwargs = _CelerySAWrapper.wrap_kwargs(kwargs)
                if current_plugin:
                    options['headers'] = options.get('headers') or {}  # None in a retry
                    options['headers']['fossir_plugin'] = current_plugin.name
                return super(fossirTask, s).apply_async(args=args, kwargs=kwargs, task_id=task_id, producer=producer,
                                                        link=link, link_error=link_error, shadow=shadow, **options)

            def __call__(s, *args, **kwargs):
                stack = ExitStack()
                stack.enter_context(self.flask_app.app_context())
                if getattr(s, 'request_context', False):
                    stack.enter_context(self.flask_app.test_request_context(base_url=config.BASE_URL))
                args = _CelerySAWrapper.unwrap_args(args)
                kwargs = _CelerySAWrapper.unwrap_kwargs(kwargs)
                plugin = getattr(s, 'plugin', s.request.get('fossir_plugin'))
                if isinstance(plugin, basestring):
                    plugin_name = plugin
                    plugin = plugin_engine.get_plugin(plugin)
                    if plugin is None:
                        stack.close()
                        raise ValueError('Plugin not active: ' + plugin_name)
                stack.enter_context(plugin_context(plugin))
                clearCache()
                with stack:
                    request_stats_request_started()
                    init_email_queue()
                    rv = super(fossirTask, s).__call__(*args, **kwargs)
                    flush_email_queue()
                    return rv

        self.Task = fossirTask


class fossirCeleryLogging(Logging):
    def _configure_logger(self, logger, *args, **kwargs):
        # don't let celery mess with the root logger
        if logger is logging.getLogger():
            return
        super(fossirCeleryLogging, self)._configure_logger(logger, *args, **kwargs)


class fossirPersistentScheduler(PersistentScheduler):
    """Celery scheduler that allows fossir.conf to override specific entries"""

    def setup_schedule(self):
        deleted = set()
        for task_name, entry in config.SCHEDULED_TASK_OVERRIDE.iteritems():
            if task_name not in self.app.conf['beat_schedule']:
                self.logger.error('Invalid entry in ScheduledTaskOverride: %s', task_name)
                continue
            if not entry:
                deleted.add(task_name)
                del self.app.conf['beat_schedule'][task_name]
            elif isinstance(entry, dict):
                assert entry.get('task') in {None, task_name}  # make sure the task name is not changed
                self.app.conf['beat_schedule'][task_name].update(entry)
            else:
                self.app.conf['beat_schedule'][task_name]['schedule'] = entry
        super(fossirPersistentScheduler, self).setup_schedule()
        if not self.app.conf['worker_redirect_stdouts']:
            # print the schedule unless we are in production where
            # this output would get redirected to a logger which is
            # not pretty, especially with the colors
            self._print_schedule(deleted)

    def _print_schedule(self, deleted):
        table_data = [['Name', 'Schedule']]
        for entry in sorted(self.app.conf['beat_schedule'].itervalues(), key=itemgetter('task')):
            table_data.append([cformat('%{yellow!}{}%{reset}').format(entry['task']),
                               cformat('%{green}{!r}%{reset}').format(entry['schedule'])])
        for task_name in sorted(deleted):
            table_data.append([cformat('%{yellow}{}%{reset}').format(task_name),
                               cformat('%{red!}Disabled%{reset}')])
        print AsciiTable(table_data, cformat('%{white!}Periodic Tasks%{reset}')).table


class _CelerySAWrapper(object):
    """Wrapper to safely pass SQLAlchemy objects to tasks.

    This is achieved by passing only the model name and its PK values
    through the Celery serializer and then fetching the actual objects
    again when executing the task.
    """
    __slots__ = ('identity_key',)

    def __init__(self, obj):
        self.identity_key = inspect(obj).identity_key
        if self.identity_key is None:
            raise ValueError('Cannot pass non-persistent object to Celery. Did you forget to flush?')

    @property
    def object(self):
        obj = self.identity_key[0].get(self.identity_key[1])
        if obj is None:
            raise ValueError('Object not in DB: {}'.format(self))
        return obj

    @return_ascii
    def __repr__(self):
        model, args = self.identity_key
        return '<{}: {}>'.format(model.__name__, ','.join(map(repr, args)))

    @classmethod
    def wrap_args(cls, args):
        return tuple(cls(x) if isinstance(x, db.Model) else x for x in args)

    @classmethod
    def wrap_kwargs(cls, kwargs):
        return {k: cls(v) if isinstance(v, db.Model) else v for k, v in kwargs.iteritems()}

    @classmethod
    def unwrap_args(cls, args):
        return tuple(x.object if isinstance(x, cls) else x for x in args)

    @classmethod
    def unwrap_kwargs(cls, kwargs):
        return {k: v.object if isinstance(v, cls) else v for k, v in kwargs.iteritems()}