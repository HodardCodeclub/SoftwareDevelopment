

from __future__ import unicode_literals

from flask import flash, redirect

from fossir.modules.admin import RHAdminBase
from fossir.modules.admin.views import WPAdmin
from fossir.modules.rb import rb_settings
from fossir.modules.rb.forms.settings import SettingsForm
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import FormDefaults


class RHRoomBookingSettings(RHAdminBase):
    def _process(self):
        defaults = FormDefaults(**rb_settings.get_all())
        form = SettingsForm(obj=defaults)
        if form.validate_on_submit():
            rb_settings.set_multi(form.data)
            flash(_('Settings saved'), 'success')
            return redirect(url_for('.settings'))

        return WPAdmin.render_template('rb/settings.html', 'rb-settings', form=form)
