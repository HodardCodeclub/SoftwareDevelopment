

from __future__ import unicode_literals

from celery.signals import import_modules
from flask import session

from fossir.core import signals
from fossir.core.celery.core import fossirCelery
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


__all__ = ('celery',)


#: The Celery instance for all fossir tasks
celery = fossirCelery('fossir')


@signals.app_created.connect
def _load_default_modules(app, **kwargs):
    celery.loader.import_default_modules()  # load all tasks


@import_modules.connect
def _import_modules(*args, **kwargs):
    import fossir.core.emails
    import fossir.util.tasks
    signals.import_tasks.send()


@signals.menu.items.connect_via('admin-sidemenu')
def _extend_admin_menu(sender, **kwargs):
    if session.user.is_admin:
        return SideMenuItem('celery', _("Tasks"), url_for('celery.index'), 20, icon='time')
