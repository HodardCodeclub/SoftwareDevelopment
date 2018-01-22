

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.core.settings import SettingsProxy
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


__all__ = ('logger', 'cephalopod_settings')

logger = Logger.get('cephalopod')

cephalopod_settings = SettingsProxy('cephalopod', {
    'show_migration_message': False,
    'joined': False,
    'contact_email': None,
    'contact_name': None,
    'uuid': None
})


@signals.menu.items.connect_via('admin-sidemenu')
def _extend_admin_menu(sender, **kwargs):
    if session.user.is_admin:
        return SideMenuItem('cephalopod', _("Community Hub"), url_for('cephalopod.index'), section='integration')
