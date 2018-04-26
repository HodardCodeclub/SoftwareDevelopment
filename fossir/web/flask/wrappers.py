

from __future__ import absolute_import, unicode_literals

import os
from contextlib import contextmanager
from uuid import uuid4

from flask import Blueprint, Flask, request
from flask.blueprints import BlueprintSetupState
from flask.helpers import locked_cached_property
from flask.wrappers import Request
from flask_pluginengine import PluginFlaskMixin
from jinja2 import FileSystemLoader, TemplateNotFound
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug.utils import cached_property

from fossir.core.config import config
from fossir.util.json import fossirJSONEncoder
from fossir.web.flask.session import fossirSessionInterface
from fossir.web.flask.templating import CustomizationLoader
from fossir.web.flask.util import make_view_func


_notset = object()


class fossirRequest(Request):
    parameter_storage_class = ImmutableOrderedMultiDict

    @cached_property
    def id(self):
        return uuid4().hex[:16]

    @cached_property
    def relative_url(self):
        """The request's path including its query string if applicable."""
        return self.script_root + self.full_path.rstrip('?')

    @cached_property
    def remote_addr(self):
        ip = super(fossirRequest, self).remote_addr
        if ip is not None and ip.startswith('::ffff:'):
            # convert ipv6-style ipv4 to the regular ipv4 notation
            ip = ip[7:]
        return ip

    @property
    def json(self):
        # Override to avoid deprecation warning
        return self.get_json()

    def __repr__(self):
        rv = super(fossirRequest, self).__repr__()
        if isinstance(rv, unicode):
            rv = rv.encode('utf-8')
        return rv


class fossirFlask(PluginFlaskMixin, Flask):
    json_encoder = fossirJSONEncoder
    request_class = fossirRequest
    session_interface = fossirSessionInterface()

    @property
    def session_cookie_name(self):
        name = super(fossirFlask, self).session_cookie_name
        if not request.is_secure:
            name += '_http'
        return name

    def create_global_jinja_loader(self):
        default_loader = super(fossirFlask, self).create_global_jinja_loader()
        customization_dir = config.CUSTOMIZATION_DIR
        if not customization_dir:
            return default_loader
        return CustomizationLoader(default_loader, os.path.join(customization_dir, 'templates'),
                                   config.CUSTOMIZATION_DEBUG)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        from fossir.web.rh import RHSimple
        # Endpoints from Flask-Multipass need to be wrapped in the RH
        # logic to get the autocommit logic and error handling for code
        # running inside the identity handler.
        if endpoint is not None and endpoint.startswith('_flaskmultipass'):
            view_func = RHSimple.wrap_function(view_func)
        return super(fossirFlask, self).add_url_rule(rule, endpoint=endpoint, view_func=view_func, **options)

    def _find_error_handler(self, e):
        # XXX: this is a backport from flask 1.0
        # remove this method once flask 1.0 is out and we updated
        exc_class, code = self._get_exc_class_and_code(type(e))
        for name, c in ((request.blueprint, code), (None, code),
                        (request.blueprint, None), (None, None)):
            handler_map = self.error_handler_spec.setdefault(name, {}).get(c)
            if not handler_map:
                continue
            for cls in exc_class.__mro__:
                handler = handler_map.get(cls)
                if handler is not None:
                    return handler


class fossirBlueprintSetupState(BlueprintSetupState):
    @contextmanager
    def _unprefixed(self):
        prefix = self.url_prefix
        self.url_prefix = None
        yield
        self.url_prefix = prefix

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if rule.startswith('!/'):
            with self._unprefixed():
                super(fossirBlueprintSetupState, self).add_url_rule(rule[1:], endpoint, view_func, **options)
        else:
            super(fossirBlueprintSetupState, self).add_url_rule(rule, endpoint, view_func, **options)


class fossirBlueprint(Blueprint):
    """A Blueprint implementation that allows prefixing URLs with `!` to
    ignore the url_prefix of the blueprint.

    It also supports automatically creating rules in two versions - with and
    without a prefix.

    :param event_feature: If set, this blueprint will raise `NotFound`
                          for all its endpoints unless the event referenced
                          by the `confId` or `event_id` URL argument has
                          the specified feature.
    """

    def __init__(self, *args, **kwargs):
        self.__prefix = None
        self.__default_prefix = ''
        self.__virtual_template_folder = kwargs.pop('virtual_template_folder', None)
        event_feature = kwargs.pop('event_feature', None)
        super(fossirBlueprint, self).__init__(*args, **kwargs)

        if event_feature:
            @self.before_request
            def _check_event_feature():
                from fossir.modules.events.features.util import require_feature
                event_id = request.view_args.get('confId') or request.view_args.get('event_id')
                if event_id is not None:
                    require_feature(event_id, event_feature)

    @locked_cached_property
    def jinja_loader(self):
        if self.template_folder is not None:
            return fossirFileSystemLoader(os.path.join(self.root_path, self.template_folder),
                                          virtual_path=self.__virtual_template_folder)

    def make_setup_state(self, app, options, first_registration=False):
        return fossirBlueprintSetupState(self, app, options, first_registration)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if view_func is not None:
            # We might have a RH class here - convert it to a callable suitable as a view func.
            view_func = make_view_func(view_func)
        super(fossirBlueprint, self).add_url_rule(self.__default_prefix + rule, endpoint, view_func, **options)
        if self.__prefix:
            super(fossirBlueprint, self).add_url_rule(self.__prefix + rule, endpoint, view_func, **options)

    @contextmanager
    def add_prefixed_rules(self, prefix, default_prefix=''):
        """Creates prefixed rules in addition to the normal ones.
        When specifying a default_prefix, too, the normally "unprefixed" rules
        are prefixed with it."""
        assert self.__prefix is None and not self.__default_prefix
        self.__prefix = prefix
        self.__default_prefix = default_prefix
        yield
        self.__prefix = None
        self.__default_prefix = ''


class fossirFileSystemLoader(FileSystemLoader):
    """FileSystemLoader that makes namespacing easier.

    The `virtual_path` kwarg lets you specify a path segment that's
    handled as if all templates inside the loader's `searchpath` were
    actually inside ``searchpath/virtual_path``.  That way you don't
    have to create subdirectories in your template folder.
    """

    def __init__(self, searchpath, encoding='utf-8', virtual_path=None):
        super(fossirFileSystemLoader, self).__init__(searchpath, encoding)
        self.virtual_path = virtual_path

    def list_templates(self):
        templates = super(fossirFileSystemLoader, self).list_templates()
        if self.virtual_path:
            templates = [os.path.join(self.virtual_path, t) for t in templates]
        return templates

    def get_source(self, environment, template):
        if self.virtual_path:
            if not template.startswith(self.virtual_path):
                raise TemplateNotFound(template)
            template = template[len(self.virtual_path):]
        return super(fossirFileSystemLoader, self).get_source(environment, template)
