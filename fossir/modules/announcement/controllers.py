

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
