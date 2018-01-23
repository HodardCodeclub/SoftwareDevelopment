

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.modules.groups.core import GroupProxy
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


__all__ = ('GroupProxy',)


@signals.menu.items.connect_via('admin-sidemenu')
def _extend_admin_menu(sender, **kwargs):
    if session.user.is_admin:
        return SideMenuItem('groups', _("Groups"), url_for('groups.groups'), section='user_management')


@signals.users.merged.connect
def _merge_users(target, source, **kwargs):
    target.local_groups |= source.local_groups
    source.local_groups.clear()
