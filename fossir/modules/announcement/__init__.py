

from __future__ import unicode_literals

from flask import render_template, session

from fossir.core import signals
from fossir.core.settings import SettingsProxy
from fossir.util.i18n import _
from fossir.web.flask.templating import template_hook
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


announcement_settings = SettingsProxy('announcement', {
    'enabled': False,
    'message': ''
})


@template_hook('global-announcement')
def _inject_announcement_header(**kwargs):
    if not announcement_settings.get('enabled'):
        return
    message = announcement_settings.get('message')
    if message:
        return render_template('announcement/display.html', message=message)


@signals.menu.items.connect_via('admin-sidemenu')
def _sidemenu_items(sender, **kwargs):
    if session.user.is_admin:
        yield SideMenuItem('announcement', _('Announcement'), url_for('announcement.manage'), section='homepage')
