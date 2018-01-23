

from __future__ import unicode_literals

from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired

from fossir.modules.designer.models.templates import TemplateType
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import fossirEnumSelectField
from fossir.web.forms.widgets import SwitchWidget


class AddTemplateForm(fossirForm):
    title = StringField(_('Title'), [DataRequired()])
    type = fossirEnumSelectField(_('Template'), enum=TemplateType, default=TemplateType.poster)
    is_clonable = BooleanField(_('Allow cloning'), widget=SwitchWidget(), default=True,
                               description=_("Allow cloning this template in subcategories and events"))
