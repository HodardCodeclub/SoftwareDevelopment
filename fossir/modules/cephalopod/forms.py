

from __future__ import unicode_literals

from wtforms import BooleanField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.validators import UsedIfChecked
from fossir.web.forms.widgets import SwitchWidget


class CephalopodForm(fossirForm):
    joined = BooleanField('Join the community', widget=SwitchWidget())
    contact_name = StringField('Contact Name', [UsedIfChecked('joined'), DataRequired()],
                               description=_('Name of the person responsible for your fossir server.'))
    contact_email = EmailField('Contact Email',
                               [UsedIfChecked('joined'), DataRequired(), Email()],
                               description=_('Email address of the person responsible for your fossir server.'))
