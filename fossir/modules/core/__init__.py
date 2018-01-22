

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


@signals.menu.items.connect_via('admin-sidemenu')
def _sidemenu_items(sender, **kwargs):
    if session.user.is_admin:
        yield SideMenuItem('settings', _('General Settings'), url_for('core.settings'), 100, icon='settings')
