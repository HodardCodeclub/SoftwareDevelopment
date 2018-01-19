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
from fossir.modules.categories import upcoming_events_settings
from fossir.modules.categories.forms import UpcomingEventsForm
from fossir.modules.categories.util import get_upcoming_events
from fossir.modules.categories.views import WPManageUpcomingEvents
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import FormDefaults


class RHManageUpcomingEvents(RHAdminBase):
    def _process(self):
        form = UpcomingEventsForm(obj=FormDefaults(**upcoming_events_settings.get_all()))
        if form.validate_on_submit():
            upcoming_events_settings.set_multi(form.data)
            get_upcoming_events.clear_cached()
            flash(_('Settings saved!'), 'success')
            return redirect(url_for('categories.manage_upcoming'))
        return WPManageUpcomingEvents.render_template('admin/upcoming_events.html', 'upcoming_events', form=form)
