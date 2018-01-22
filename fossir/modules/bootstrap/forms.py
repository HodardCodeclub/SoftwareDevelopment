

from __future__ import unicode_literals

from wtforms import BooleanField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

from fossir.modules.auth.forms import LocalRegistrationForm
from fossir.util.i18n import _
from fossir.web.forms.validators import UsedIfChecked
from fossir.web.forms.widgets import SwitchWidget


class BootstrapForm(LocalRegistrationForm):
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    email = EmailField(_('Email address'), [DataRequired()])
    affiliation = StringField('Affiliation', [DataRequired()])
    enable_tracking = BooleanField('Join the community', widget=SwitchWidget())
    contact_name = StringField('Contact Name', [UsedIfChecked('enable_tracking'), DataRequired()])
    contact_email = EmailField('Contact Email Address',  [UsedIfChecked('enable_tracking'), DataRequired(), Email()])
