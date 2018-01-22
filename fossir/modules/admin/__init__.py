

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.modules.admin.controllers.base import RHAdminBase
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuSection, TopMenuItem


__all__ = ('RHAdminBase',)


@signals.menu.sections.connect_via('admin-sidemenu')
def _sidemenu_sections(sender, **kwargs):
    yield SideMenuSection('security', _("Security"), 90, icon='shield')
    yield SideMenuSection('user_management', _("User Management"), 60, icon='users')
    yield SideMenuSection('customization', _("Customization"), 50, icon='wrench')
    yield SideMenuSection('integration', _("Integration"), 30, icon='earth')
    yield SideMenuSection('homepage', _("Homepage"), 40, icon='home')


@signals.menu.items.connect_via('top-menu')
def _topmenu_items(sender, **kwargs):
    if session.user and session.user.is_admin:
        yield TopMenuItem('admin', _('Administration'), url_for('core.admin_dashboard'), 70)
