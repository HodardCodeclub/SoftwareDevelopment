

from __future__ import unicode_literals

from datetime import time, timedelta

from flask import session
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, InputRequired, ValidationError

from fossir.core.db import db
from fossir.core.db.sqlalchemy.protection import ProtectionMode
from fossir.modules.categories.fields import CategoryField
from fossir.modules.events.fields import EventPersonLinkListField, fossirThemeSelectField
from fossir.modules.events.models.events import EventType
from fossir.modules.events.models.references import ReferenceType
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import (fossirDateTimeField, fossirEnumRadioField, fossirLocationField,
                                     fossirTimezoneSelectField, OccurrencesField)
from fossir.web.forms.validators import LinkedDateTime
from fossir.web.forms.widgets import CKEditorWidget


class ReferenceTypeForm(fossirForm):
    name = StringField(_("Name"), [DataRequired()], description=_("The name of the external ID type"))
    url_template = URLField(_("URL template"),
                            description=_("The URL template must contain the '{value}' placeholder."))
    scheme = StringField(_("Scheme"), filters=[lambda x: x.rstrip(':') if x else x],
                         description=_("The scheme/protocol of the external ID type"))

    def __init__(self, *args, **kwargs):
        self.reference_type = kwargs.pop('reference_type', None)
        super(ReferenceTypeForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        query = ReferenceType.find(db.func.lower(ReferenceType.name) == field.data.lower())
        if self.reference_type:
            query = query.filter(ReferenceType.id != self.reference_type.id)
        if query.count():
            raise ValidationError(_("This name is already in use."))

    def validate_url_template(self, field):
        if field.data and '{value}' not in field.data:
            raise ValidationError(_("The URL template must contain the placeholder '{value}'."))


class EventCreationFormBase(fossirForm):
    category = CategoryField(_('Category'), [DataRequired()], allow_subcats=False, require_event_creation_rights=True)
    title = StringField(_('Event title'), [DataRequired()])
    timezone = fossirTimezoneSelectField(_('Timezone'), [DataRequired()])
    location_data = fossirLocationField(_('Location'), allow_location_inheritance=False)
    protection_mode = fossirEnumRadioField(_('Protection mode'), enum=ProtectionMode)

    def validate_category(self, field):
        if not field.data.can_create_events(session.user):
            raise ValidationError(_('You are not allowed to create events in this category.'))


class EventCreationForm(EventCreationFormBase):
    _field_order = ('title', 'start_dt', 'end_dt', 'timezone', 'location_data', 'protection_mode')
    _advanced_field_order = ()
    start_dt = fossirDateTimeField(_("Start"), [InputRequired()], default_time=time(8), allow_clear=False)
    end_dt = fossirDateTimeField(_("End"), [InputRequired(), LinkedDateTime('start_dt', not_equal=True)],
                                 default_time=time(18), allow_clear=False)


class LectureCreationForm(EventCreationFormBase):
    _field_order = ('title', 'occurrences', 'timezone', 'location_data', 'person_link_data',
                    'protection_mode')
    _advanced_field_order = ('description', 'theme')
    occurrences = OccurrencesField(_("Dates"), [DataRequired()], default_time=time(8),
                                   default_duration=timedelta(minutes=90))
    person_link_data = EventPersonLinkListField(_('Speakers'))
    description = TextAreaField(_('Description'), widget=CKEditorWidget())
    theme = fossirThemeSelectField(_('Theme'), event_type=EventType.lecture, allow_default=True)
