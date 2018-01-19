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