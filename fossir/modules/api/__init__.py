

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.db import db
from fossir.core.settings import SettingsProxy
from fossir.modules.api.models.keys import APIKey
from fossir.util.i18n import _
from fossir.util.struct.enum import fossirEnum
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


__all__ = ('settings',)


class APIMode(int, fossirEnum):
    KEY = 0  # public requests without API key, authenticated requests with api key
    ONLYKEY = 1  # all requests require an API key
    SIGNED = 2  # public requests without API key, authenticated requests with api key and signature
    ONLYKEY_SIGNED = 3  # all requests require an API key, authenticated requests need signature
    ALL_SIGNED = 4  # all requests require an api key and a signature


api_settings = SettingsProxy('api', {
    'allow_persistent': False,
    'security_mode': APIMode.KEY.value,
    'cache_ttl': 600,
    'signature_ttl': 600
})


@signals.users.merged.connect
def _merge_users(target, source, **kwargs):
    # Get the current active API keys
    ak_user = target.api_key
    ak_merged = source.api_key
    # Move all inactive keys to the new user
    APIKey.find(user_id=source.id, is_active=False).update({'user_id': target.id})
    if ak_merged and not ak_user:
        ak_merged.user = target
    elif ak_user and ak_merged:
        # Both have a key, keep the main one unless it's unused and the merged one isn't.
        if ak_user.use_count or not ak_merged.use_count:
            ak_merged.is_active = False
            ak_merged.user = target
        else:
            ak_user.is_active = False
            db.session.flush()  # flush the deactivation so we can reassociate the user
            ak_merged.user = target


@signals.menu.items.connect_via('admin-sidemenu')
def _extend_admin_menu(sender, **kwargs):
    if session.user.is_admin:
        return SideMenuItem('api', _("API"), url_for('api.admin_settings'), section='integration')


@signals.menu.items.connect_via('user-profile-sidemenu')
def _extend_profile_sidemenu(sender, **kwargs):
    yield SideMenuItem('api', _('HTTP API'), url_for('api.user_profile'), 30)
