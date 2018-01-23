

from __future__ import unicode_literals

import os
from datetime import timedelta
from uuid import uuid4

from flask import session
from flask_oauthlib.provider import OAuth2Provider

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


class fossirOAuth2Provider(OAuth2Provider):
    def init_app(self, app):
        app.config.setdefault('OAUTH2_PROVIDER_ERROR_ENDPOINT', 'oauth.oauth_errors')
        app.config.setdefault('OAUTH2_PROVIDER_TOKEN_EXPIRES_IN', int(timedelta(days=3650).total_seconds()))
        app.config.setdefault('OAUTH2_PROVIDER_TOKEN_GENERATOR', lambda req: unicode(uuid4()))
        super(fossirOAuth2Provider, self).init_app(app)


oauth = fossirOAuth2Provider()
logger = Logger.get('oauth')


@signals.menu.items.connect_via('admin-sidemenu')
def _extend_admin_menu(sender, **kwargs):
    if session.user.is_admin:
        return SideMenuItem('applications', 'Applications', url_for('oauth.apps'), section='integration')


@signals.menu.items.connect_via('user-profile-sidemenu')
def _extend_profile_sidemenu(sender, user, **kwargs):
    yield SideMenuItem('applications', _('Applications'), url_for('oauth.user_profile'), 40, disabled=user.is_system)


@signals.app_created.connect
def _no_ssl_required_on_debug(app, **kwargs):
    if app.debug:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


@signals.users.merged.connect
def _delete_merged_user_tokens(target, source, **kwargs):
    source.oauth_tokens.delete()
    logger.info("All tokens for the user %s were deleted.", source)
