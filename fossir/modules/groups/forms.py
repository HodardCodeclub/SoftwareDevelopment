

from __future__ import unicode_literals

from wtforms.fields import BooleanField, SelectField, StringField
from wtforms.validators import DataRequired, ValidationError

from fossir.core.db import db
from fossir.modules.groups.models.groups import LocalGroup
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import PrincipalListField


class SearchForm(fossirForm):
    provider = SelectField(_('Provider'))
    name = StringField(_('Group name'), [DataRequired()])
    exact = BooleanField(_('Exact match'))


class EditGroupForm(fossirForm):
    name = StringField(_('Group name'), [DataRequired()])
    members = PrincipalListField(_('Group members'))

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group', None)
        super(EditGroupForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        query = LocalGroup.find(db.func.lower(LocalGroup.name) == field.data.lower())
        if self.group:
            query = query.filter(LocalGroup.id != self.group.id)
        if query.count():
            raise ValidationError(_('A group with this name already exists.'))
