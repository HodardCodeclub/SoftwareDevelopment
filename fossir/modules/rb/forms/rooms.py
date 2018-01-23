

import itertools
from operator import itemgetter

from wtforms import Form
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import BooleanField, FieldList, FloatField, FormField, IntegerField, RadioField, StringField
from wtforms.fields.simple import FileField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError
from wtforms.widgets.core import HiddenInput
from wtforms_components import TimeField

from fossir.modules.rb.models.equipment import EquipmentType
from fossir.modules.rb.models.locations import Location
from fossir.util.i18n import _
from fossir.util.struct.iterables import group_nested
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import fossirQuerySelectMultipleCheckboxField, PrincipalField
from fossir.web.forms.validators import UsedIf
from fossir.web.forms.widgets import ConcatWidget


def _get_equipment_label(eq):
    parents = []
    parent = eq.parent
    while parent:
        parents.append(parent.name)
        parent = parent.parent
    return ': '.join(itertools.chain(reversed(parents), [eq.name]))


def _group_equipment(objects):
    """Groups the equipment list so children follow their their parents"""
    return group_nested(objects, itemgetter(1))


class SearchRoomsForm(fossirForm):
    location = QuerySelectField(_(u'Location'), get_label=lambda x: x.name, query_factory=Location.find,
                                allow_blank=True)
    details = StringField()
    available = RadioField(_(u'Availability'), coerce=int, default=-1, widget=ConcatWidget(prefix_label=False),
                           choices=[(1, _(u'Available')), (0, _(u'Booked')), (-1, _(u"Don't care"))])
    capacity = IntegerField(_(u'Capacity'), validators=[Optional(), NumberRange(min=0)])
    available_equipment = fossirQuerySelectMultipleCheckboxField(_(u'Equipment'), get_label=_get_equipment_label,
                                                                 modify_object_list=_group_equipment,
                                                                 query_factory=lambda: EquipmentType.find().order_by(
                                                                     EquipmentType.name))
    is_only_public = BooleanField(_(u'Only public rooms'), default=True)
    is_auto_confirm = BooleanField(_(u'Only rooms not requiring confirmation'), default=True)
    is_only_active = BooleanField(_(u'Only active rooms'), default=True)
    is_only_my_rooms = BooleanField(_(u'Only my rooms'))
    # Period details when searching for (un-)availability
    start_dt = DateTimeField(_(u'Start date'), validators=[Optional()], parse_kwargs={'dayfirst': True},
                             display_format='%d/%m/%Y %H:%M', widget=HiddenInput())
    end_dt = DateTimeField(_(u'End date'), validators=[Optional()], parse_kwargs={'dayfirst': True},
                           display_format='%d/%m/%Y %H:%M', widget=HiddenInput())
    repeatability = StringField()  # TODO: use repeat_frequency/interval with new UI
    include_pending_blockings = BooleanField(_(u'Check conflicts against pending blockings'), default=True)
    include_pre_bookings = BooleanField(_(u'Check conflicts against pre-bookings'), default=True)


class _TimePair(Form):
    start = TimeField(_(u'from'), [UsedIf(lambda form, field: form.end.data)])
    end = TimeField(_(u'to'), [UsedIf(lambda form, field: form.start.data)])

    def validate_start(self, field):
        if self.start.data and self.end.data and self.start.data >= self.end.data:
            raise ValidationError('The start time must be earlier than the end time.')

    validate_end = validate_start


class _DateTimePair(Form):
    start = DateTimeField(_(u'from'), [UsedIf(lambda form, field: form.end.data)], display_format='%d/%m/%Y %H:%M',
                          parse_kwargs={'dayfirst': True})
    end = DateTimeField(_(u'to'), [UsedIf(lambda form, field: form.start.data)], display_format='%d/%m/%Y %H:%M',
                        parse_kwargs={'dayfirst': True})

    def validate_start(self, field):
        if self.start.data and self.end.data and self.start.data >= self.end.data:
            raise ValidationError('The start date must be earlier than the end date.')

    validate_end = validate_start


class RoomForm(fossirForm):
    name = StringField(_(u'Name'))
    site = StringField(_(u'Site'))
    building = StringField(_(u'Building'), [DataRequired()])
    floor = StringField(_(u'Floor'), [DataRequired()])
    number = StringField(_(u'Number'), [DataRequired()])
    longitude = FloatField(_(u'Longitude'), [Optional()])
    latitude = FloatField(_(u'Latitude'), [Optional()])
    is_active = BooleanField(_(u'Active'), default=True)
    is_reservable = BooleanField(_(u'Public'), default=True)
    reservations_need_confirmation = BooleanField(_(u'Confirmations'))
    notification_for_assistance = BooleanField(_(u'Assistance'))
    notification_before_days = IntegerField(_(u'Send booking reminders X days before (single/daily)'),
                                            [Optional(), NumberRange(min=1, max=30)])
    notification_before_days_weekly = IntegerField(_(u'Send booking reminders X days before (weekly)'),
                                                   [Optional(), NumberRange(min=1, max=30)])
    notification_before_days_monthly = IntegerField(_(u'Send booking reminders X days before (monthly)'),
                                                    [Optional(), NumberRange(min=1, max=30)])
    notifications_enabled = BooleanField(_(u'Reminders enabled'), default=True)
    booking_limit_days = IntegerField(_(u'Maximum length of booking (days)'), [Optional(), NumberRange(min=1)])
    owner = PrincipalField(_(u'Owner'), [DataRequired()], allow_external=True)
    key_location = StringField(_(u'Where is key?'))
    telephone = StringField(_(u'Telephone'))
    capacity = IntegerField(_(u'Capacity'), [Optional(), NumberRange(min=1)], default=20)
    division = StringField(_(u'Department'))
    surface_area = IntegerField(_(u'Surface area'), [Optional(), NumberRange(min=0)])
    max_advance_days = IntegerField(_(u'Maximum advance time for bookings'), [Optional(), NumberRange(min=1)])
    comments = TextAreaField(_(u'Comments'))
    delete_photos = BooleanField(_(u'Delete photos'))
    large_photo = FileField(_(u'Large photo'))
    small_photo = FileField(_(u'Small photo'))
    available_equipment = fossirQuerySelectMultipleCheckboxField(_(u'Equipment'), get_label=_get_equipment_label,
                                                                 modify_object_list=_group_equipment)
    # attribute_* - set at runtime
    bookable_hours = FieldList(FormField(_TimePair), min_entries=1)
    nonbookable_periods = FieldList(FormField(_DateTimePair), min_entries=1)

    def validate_large_photo(self, field):
        if not field.data and self.small_photo.data:
            raise ValidationError(_(u'When uploading a small photo you need to upload a large photo, too.'))

    def validate_small_photo(self, field):
        if not field.data and self.large_photo.data:
            raise ValidationError(_(u'When uploading a large photo you need to upload a small photo, too.'))
