

from __future__ import unicode_literals

from wtforms.fields import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired

from fossir.util.i18n import _
from fossir.web.fields import BaseField
from fossir.web.forms.base import fossirForm
from fossir.web.forms.widgets import SwitchWidget


class SurveyFieldConfigForm(fossirForm):
    title = StringField(_('Title'), [DataRequired()], description=_("The title of the question"))
    description = TextAreaField(_('Description'), description=_("The description (shown below the question's field.)"))
    is_required = BooleanField(_('Required'), widget=SwitchWidget(),
                               description=_("If the user has to answer the question."))


class SurveyField(BaseField):
    config_form_base = SurveyFieldConfigForm

    def get_summary(self):
        """Return the summary of answers submitted for this field."""
        raise NotImplementedError

    @staticmethod
    def process_imported_data(data):
        """Process the form's data imported from a dict."""
        return data
