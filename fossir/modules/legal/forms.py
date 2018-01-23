
from __future__ import unicode_literals

from wtforms.fields import TextAreaField

from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.widgets import CKEditorWidget


class LegalMessagesForm(fossirForm):
    network_protected_disclaimer = TextAreaField(_("Network-protected information disclaimer"), widget=CKEditorWidget())
    restricted_disclaimer = TextAreaField(_("Restricted information disclaimer"), widget=CKEditorWidget())
    tos = TextAreaField(_("Terms and conditions"), widget=CKEditorWidget())
