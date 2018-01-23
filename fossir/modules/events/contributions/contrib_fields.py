

from __future__ import unicode_literals

from wtforms.fields import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Optional

from fossir.modules.events.contributions.models.fields import ContributionField
from fossir.util.i18n import _
from fossir.web.fields import BaseField, get_field_definitions
from fossir.web.fields.choices import SingleChoiceField
from fossir.web.fields.simple import TextField
from fossir.web.forms.base import fossirForm
from fossir.web.forms.widgets import SwitchWidget


def get_contrib_field_types():
    """Get a dict containing all contribution field types"""
    return get_field_definitions(ContributionField)


class ContribFieldConfigForm(fossirForm):
    title = StringField(_('Title'), [DataRequired()], description=_("The title of the field"))
    description = TextAreaField(_('Description'), description=_("The description of the field"))
    is_required = BooleanField(_('Required'), widget=SwitchWidget(),
                               description=_("Whether the user has to fill out the field"))
    is_active = BooleanField(_('Active'), widget=SwitchWidget(),
                             description=_("Whether the field is available."),
                             default=True)


class ContribField(BaseField):
    config_form_base = ContribFieldConfigForm
    common_settings = ('title', 'description', 'is_required', 'is_active')

    def __init__(self, obj, management=True):
        super(ContribField, self).__init__(obj)
        self.management = management

    @property
    def required_validator(self):
        return Optional if self.management else DataRequired


class ContribTextField(TextField, ContribField):
    pass


class ContribSingleChoiceField(SingleChoiceField, ContribField):
    pass
