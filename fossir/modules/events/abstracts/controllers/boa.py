

from __future__ import unicode_literals

from flask import flash

from fossir.modules.events.abstracts.controllers.base import RHAbstractsBase, RHManageAbstractsBase
from fossir.modules.events.abstracts.forms import BOASettingsForm
from fossir.modules.events.abstracts.settings import boa_settings
from fossir.modules.events.abstracts.util import clear_boa_cache, create_boa
from fossir.util.i18n import _
from fossir.web.flask.util import send_file
from fossir.web.forms.base import FormDefaults
from fossir.web.util import jsonify_data, jsonify_form


class RHManageBOA(RHManageAbstractsBase):
    """Configure book of abstracts"""

    def _process(self):
        form = BOASettingsForm(obj=FormDefaults(**boa_settings.get_all(self.event)))
        if form.validate_on_submit():
            boa_settings.set_multi(self.event, form.data)
            clear_boa_cache(self.event)
            flash(_('Book of Abstract settings have been saved'), 'success')
            return jsonify_data()
        return jsonify_form(form)


class RHExportBOA(RHAbstractsBase):
    """Export the book of abstracts"""

    def _process(self):
        return send_file('book-of-abstracts.pdf', create_boa(self.event), 'application/pdf')
