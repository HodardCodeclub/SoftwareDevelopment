
from __future__ import unicode_literals

from flask import redirect

from fossir.modules.admin import RHAdminBase
from fossir.modules.legal import legal_settings
from fossir.modules.legal.forms import LegalMessagesForm
from fossir.modules.legal.views import WPDisplayLegalMessages, WPManageLegalMessages
from fossir.web.flask.util import url_for
from fossir.web.rh import RH


class RHManageLegalMessages(RHAdminBase):
    def _process(self):
        form = LegalMessagesForm(**legal_settings.get_all())
        if form.validate_on_submit():
            legal_settings.set_multi(form.data)
            return redirect(url_for('legal.manage'))
        return WPManageLegalMessages.render_template('manage_messages.html', 'legal_messages', form=form)


class RHDisplayLegalMessages(RH):
    def _process(self):
        return WPDisplayLegalMessages.render_template('tos.html', tos=legal_settings.get('tos'))
