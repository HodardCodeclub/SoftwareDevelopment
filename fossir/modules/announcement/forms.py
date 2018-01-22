

from __future__ import unicode_literals

from wtforms.fields import BooleanField, TextAreaField
from wtforms.validators import DataRequired

from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.validators import UsedIf
from fossir.web.forms.widgets import SwitchWidget


class AnnouncementForm(fossirForm):
    enabled = BooleanField(_('Enabled'), widget=SwitchWidget())
    message = TextAreaField(_('Message'), [UsedIf(lambda form, _: form.enabled.data), DataRequired()])
