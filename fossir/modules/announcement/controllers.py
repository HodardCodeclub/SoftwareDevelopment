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

from flask import flash, redirect

from fossir.modules.admin import RHAdminBase
from fossir.modules.announcement import announcement_settings
from fossir.modules.announcement.forms import AnnouncementForm
from fossir.modules.announcement.views import WPAnnouncement
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import FormDefaults


class RHAnnouncement(RHAdminBase):
    def _process(self):
        form = AnnouncementForm(obj=FormDefaults(**announcement_settings.get_all()))
        if form.validate_on_submit():
            announcement_settings.set_multi(form.data)
            flash(_('Settings have been saved'), 'success')
            return redirect(url_for('announcement.manage'))
        return WPAnnouncement.render_template('settings.html', 'announcement', form=form)
