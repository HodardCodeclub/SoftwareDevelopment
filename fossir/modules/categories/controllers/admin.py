

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
