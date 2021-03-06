

from __future__ import unicode_literals

from datetime import timedelta

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from fossir.core.db import db
from fossir.core.db.sqlalchemy.descriptions import RenderMode
from fossir.modules.events.contributions.fields import (ContributionPersonLinkListField,
                                                        SubContributionPersonLinkListField)
from fossir.modules.events.contributions.models.references import ContributionReference, SubContributionReference
from fossir.modules.events.contributions.models.types import ContributionType
from fossir.modules.events.fields import ReferencesField
from fossir.util.date_time import get_day_end
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import fossirForm, generated_data
from fossir.web.forms.fields import (AccessControlListField, fossirDateTimeField, fossirLocationField,
                                     fossirProtectionField, fossirTagListField, PrincipalListField, TimeDeltaField)
from fossir.web.forms.validators import DateTimeRange, MaxDuration, UsedIf


class ContributionForm(fossirForm):
    title = StringField(_("Title"), [DataRequired()])
    description = TextAreaField(_("Description"))
    start_dt = fossirDateTimeField(_("Start date"),
                                   [DataRequired(),
                                    DateTimeRange(earliest=lambda form, field: form._get_earliest_start_dt(),
                                                  latest=lambda form, field: form._get_latest_start_dt())],
                                   allow_clear=False,
                                   description=_("Start date of the contribution"))
    duration = TimeDeltaField(_("Duration"), [DataRequired(), MaxDuration(timedelta(hours=24))],
                              default=timedelta(minutes=20), units=('minutes', 'hours'))
    type = QuerySelectField(_("Type"), get_label='name', allow_blank=True, blank_text=_("No type selected"))
    person_link_data = ContributionPersonLinkListField(_("People"))
    location_data = fossirLocationField(_("Location"))
    keywords = fossirTagListField(_('Keywords'))
    references = ReferencesField(_("External IDs"), reference_class=ContributionReference,
                                 description=_("Manage external resources for this contribution"))
    board_number = StringField(_("Board Number"))

    @generated_data
    def render_mode(self):
        return RenderMode.markdown

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        self.contrib = kwargs.pop('contrib', None)
        self.session_block = kwargs.get('session_block')
        self.timezone = self.event.timezone
        to_schedule = kwargs.pop('to_schedule', False)
        super(ContributionForm, self).__init__(*args, **kwargs)
        self.type.query = self.event.contribution_types
        if self.event.type != 'conference':
            self.person_link_data.label.text = _("Speakers")
        if not self.type.query.count():
            del self.type
        if not to_schedule and (self.contrib is None or not self.contrib.is_scheduled):
            del self.start_dt

    def _get_earliest_start_dt(self):
        return self.session_block.start_dt if self.session_block else self.event.start_dt

    def _get_latest_start_dt(self):
        return self.session_block.end_dt if self.session_block else self.event.end_dt

    def validate_duration(self, field):
        start_dt = self.start_dt.data if self.start_dt else None
        if start_dt:
            end_dt = start_dt + field.data
            if self.session_block and end_dt > self.session_block.end_dt:
                raise ValidationError(_("With the current duration the contribution exceeds the block end date"))
            if end_dt > self.event.end_dt:
                raise ValidationError(_('With the current duration the contribution exceeds the event end date'))

    @property
    def custom_field_names(self):
        return tuple([field_name for field_name in self._fields if field_name.startswith('custom_')])


class ContributionProtectionForm(fossirForm):
    protection_mode = fossirProtectionField(_('Protection mode'), protected_object=lambda form: form.protected_object,
                                            acl_message_url=lambda form: url_for('contributions.acl_message',
                                                                                 form.protected_object))
    acl = AccessControlListField(_('Access control list'),
                                 [UsedIf(lambda form, field: form.protected_object.is_protected)],
                                 groups=True, allow_emails=True, default_text=_('Restrict access to this contribution'),
                                 description=_('List of users allowed to access the contribution'))
    managers = PrincipalListField(_('Managers'), groups=True, allow_emails=True,
                                  description=_('List of users allowed to modify the contribution'))
    submitters = PrincipalListField(_('Submitters'), groups=True, allow_emails=True,
                                    description=_('List of users allowed to submit materials for this contribution'))

    def __init__(self, *args, **kwargs):
        self.protected_object = kwargs.pop('contrib')
        super(ContributionProtectionForm, self).__init__(*args, **kwargs)


class SubContributionForm(fossirForm):
    title = StringField(_('Title'), [DataRequired()])
    description = TextAreaField(_('Description'))
    duration = TimeDeltaField(_('Duration'), [DataRequired(), MaxDuration(timedelta(hours=24))],
                              default=timedelta(minutes=20), units=('minutes', 'hours'))
    speakers = SubContributionPersonLinkListField(_('Speakers'), allow_submitters=False,
                                                  description=_('The speakers of the subcontribution'))
    references = ReferencesField(_("External IDs"), reference_class=SubContributionReference,
                                 description=_("Manage external resources for this sub-contribution"))

    @generated_data
    def render_mode(self):
        return RenderMode.markdown

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        self.subcontrib = kwargs.pop('subcontrib', None)
        super(SubContributionForm, self).__init__(*args, **kwargs)


class ContributionStartDateForm(fossirForm):
    start_dt = fossirDateTimeField(_('Start date'), [DataRequired(),
                                                     DateTimeRange(earliest=lambda form, field: form.event.start_dt,
                                                                   latest=lambda form, field: form.event.end_dt)],
                                   allow_clear=False)

    def __init__(self, *args, **kwargs):
        self.contrib = kwargs.pop('contrib')
        self.event = self.contrib.event
        self.timezone = self.event.timezone
        super(ContributionStartDateForm, self).__init__(*args, **kwargs)

    def validate_start_dt(self, field):
        event = self.contrib.event
        day = self.contrib.start_dt.astimezone(event.tzinfo).date()
        if day == event.end_dt_local.date():
            latest_dt = event.end_dt
            error_msg = _("With this time, the contribution would exceed the event end time.")
        else:
            latest_dt = get_day_end(day, tzinfo=event.tzinfo)
            error_msg = _("With this time, the contribution would exceed the current day.")
        if field.data + self.contrib.duration > latest_dt:
            raise ValidationError(error_msg)


class ContributionDurationForm(fossirForm):
    duration = TimeDeltaField(_('Duration'), [DataRequired(), MaxDuration(timedelta(days=1))],
                              default=timedelta(minutes=20), units=('minutes', 'hours'))

    def __init__(self, *args, **kwargs):
        self.contrib = kwargs.pop('contrib')
        super(ContributionDurationForm, self).__init__(*args, **kwargs)

    def validate_duration(self, field):
        if field.errors:
            return
        if self.contrib.is_scheduled:
            event = self.contrib.event
            day = self.contrib.start_dt.astimezone(event.tzinfo).date()
            if day == event.end_dt_local.date():
                latest_dt = event.end_dt
                error_msg = _("With this duration, the contribution would exceed the event end time.")
            else:
                latest_dt = get_day_end(day, tzinfo=event.tzinfo)
                error_msg = _("With this duration, the contribution would exceed the current day.")
            if self.contrib.start_dt + field.data > latest_dt:
                raise ValidationError(error_msg)


class ContributionTypeForm(fossirForm):
    """Form to create or edit a ContributionType"""

    name = StringField(_("Name"), [DataRequired()])
    description = TextAreaField(_("Description"))

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        self.contrib_type = kwargs.get('obj')
        super(ContributionTypeForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        query = self.event.contribution_types.filter(db.func.lower(ContributionType.name) == field.data.lower())
        if self.contrib_type:
            query = query.filter(ContributionType.id != self.contrib_type.id)
        if query.count():
            raise ValidationError(_("A contribution type with this name already exists"))
