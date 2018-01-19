# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from functools import partial

from flask import request
from wtforms.fields import BooleanField, HiddenField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional, ValidationError

from fossir.modules.categories.models.categories import Category, EventMessageMode
from fossir.modules.categories.util import get_image_data, get_visibility_options
from fossir.modules.events import Event
from fossir.modules.events.fields import fossirThemeSelectField
from fossir.modules.events.models.events import EventType
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import (AccessControlListField, EditableFileField, EmailListField, HiddenFieldList,
                                     fossirEnumSelectField, fossirMarkdownField, fossirProtectionField,
                                     fossirTimezoneSelectField, MultipleItemsField, PrincipalListField)
from fossir.web.forms.widgets import HiddenCheckbox, SwitchWidget


class CategorySettingsForm(fossirForm):
    BASIC_FIELDS = ('title', 'description', 'timezone', 'lecture_theme', 'meeting_theme', 'visibility',
                    'suggestions_disabled', 'event_creation_notification_emails', 'notify_managers')
    EVENT_HEADER_FIELDS = ('event_message_mode', 'event_message')

    title = StringField(_("Title"), [DataRequired()])
    description = fossirMarkdownField(_("Description"))
    timezone = fossirTimezoneSelectField(_("Timezone"), [DataRequired()],
                                         description=_("Default timezone event lists will show up in. It will also be "
                                                       "used as a default for new events."))
    lecture_theme = fossirThemeSelectField(_("Theme for Lectures"), [DataRequired()], event_type=EventType.lecture,
                                           description=_("Default timetable theme used for lecture events"))
    meeting_theme = fossirThemeSelectField(_("Theme for Meetings"), [DataRequired()], event_type=EventType.meeting,
                                           description=_("Default timetable theme used for meeting events"))
    suggestions_disabled = BooleanField(_('Disable Suggestions'), widget=SwitchWidget(),
                                        description=_("Enable this if you don't want fossir to suggest this category as"
                                                      " a possible addition to a user's favourites."))
    event_message_mode = fossirEnumSelectField(_("Message Type"), enum=EventMessageMode,
                                               default=EventMessageMode.disabled,
                                               description=_("This message will show up at the top of every event page "
                                                             "in this category"))
    event_message = fossirMarkdownField(_("Content"))
    notify_managers = BooleanField(_("Notify managers"), widget=SwitchWidget(),
                                   description=_("Whether to send email notifications to all managers of this category "
                                                 "when an event is created inside it or in any of its subcategories."))
    event_creation_notification_emails = EmailListField(_("Notification E-mails"),
                                                        description=_("List of emails that will receive a notification "
                                                                      "every time a new event is created inside the "
                                                                      "category or one of its subcategories. "
                                                                      "One email address per line."))


class CategoryIconForm(fossirForm):
    icon = EditableFileField("Icon", accepted_file_types='image/jpeg,image/jpg,image/png,image/gif',
                             add_remove_links=False, handle_flashes=True, get_metadata=partial(get_image_data, 'icon'),
                             description=_("Small icon that will show up next to category names in overview pages. "
                                           "Will be automatically resized to 16x16 pixels. This may involve loss of "
                                           "image quality, so try to upload images as close as possible to those "
                                           "dimensions."))


class CategoryLogoForm(fossirForm):
    logo = EditableFileField("Logo", accepted_file_types='image/jpeg,image/jpg,image/png,image/gif',
                             add_remove_links=False, handle_flashes=True, get_metadata=partial(get_image_data, 'logo'),
                             description=_("Logo that will show up next to the category description. Will be "
                                           "automatically resized to at most 200x200 pixels."))


class CategoryProtectionForm(fossirForm):
    _event_creation_fields = ('event_creation_restricted', 'event_creators', 'event_creation_notification_emails')

    protection_mode = fossirProtectionField(_('Protection mode'), protected_object=lambda form: form.protected_object)
    acl = AccessControlListField(_('Access control list'), groups=True, allow_external=True, allow_networks=True,
                                 default_text=_('Restrict access to this category'),
                                 description=_('List of users allowed to access the category.'))
    managers = PrincipalListField(_('Managers'), groups=True)
    own_no_access_contact = StringField(_('No access contact'),
                                        description=_('Contact information shown when someone lacks access to the '
                                                      'category'))
    visibility = SelectField(_("Event visibility"), [Optional()], coerce=lambda x: None if x == '' else int(x),
                             description=_("""From which point in the category tree contents will be visible from """
                                           """(number of categories upwards). Applies to "Today's events" and """
                                           """Calendar. If the category is moved, this number will be preserved."""))
    event_creation_restricted = BooleanField(_('Restricted event creation'), widget=SwitchWidget(),
                                             description=_('Whether the event creation should be restricted '
                                                           'to a list of specific persons'))
    event_creators = PrincipalListField(_('Event creators'), groups=True, allow_external=True,
                                        description=_('Users allowed to create events in this category'))

    def __init__(self, *args, **kwargs):
        self.protected_object = category = kwargs.pop('category')
        super(CategoryProtectionForm, self).__init__(*args, **kwargs)
        self._init_visibility(category)

    def _init_visibility(self, category):
        self.visibility.choices = get_visibility_options(category, allow_invisible=False)
        # Check if category visibility would be affected by any of the parents
        real_horizon = category.real_visibility_horizon
        own_horizon = category.own_visibility_horizon
        if real_horizon and real_horizon.is_descendant_of(own_horizon):
            self.visibility.warning = _("This category's visibility is currently limited by that of '{}'.").format(
                real_horizon.title)


class CreateCategoryForm(fossirForm):
    """Form to create a new Category"""

    title = StringField(_("Title"), [DataRequired()])
    description = fossirMarkdownField(_("Description"))


class SplitCategoryForm(fossirForm):
    first_category = StringField(_('Category name #1'), [DataRequired()],
                                 description=_('Selected events will be moved into a new sub-category with this '
                                               'title.'))
    second_category = StringField(_('Category name #2'), [DataRequired()],
                                  description=_('Events that were not selected will be moved into a new sub-category '
                                                'with this title.'))
    event_id = HiddenFieldList()
    all_selected = BooleanField(widget=HiddenCheckbox())
    submitted = HiddenField()

    def __init__(self, *args, **kwargs):
        super(SplitCategoryForm, self).__init__(*args, **kwargs)
        if self.all_selected.data:
            self.event_id.data = []
            self.first_category.label.text = _('Category name')
            self.first_category.description = _('The events will be moved into a new sub-category with this title.')
            del self.second_category

    def is_submitted(self):
        return super(SplitCategoryForm, self).is_submitted() and 'submitted' in request.form


class UpcomingEventsForm(fossirForm):
    max_entries = IntegerField(_('Max. events'), [InputRequired(), NumberRange(min=0)],
                               description=_("The maximum number of upcoming events to show. Events are sorted by "
                                             "weight so events with a lower weight are more likely to be omitted if "
                                             "there are too many events to show."))
    entries = MultipleItemsField(_('Upcoming events'),
                                 fields=[{'id': 'type', 'caption': _("Type"), 'required': True, 'type': 'select'},
                                         {'id': 'id', 'caption': _("ID"), 'required': True, 'type': 'number',
                                          'step': 1, 'coerce': int},
                                         {'id': 'days', 'caption': _("Days"), 'required': True, 'type': 'number',
                                          'step': 1, 'coerce': int},
                                         {'id': 'weight', 'caption': _("Weight"), 'required': True, 'type': 'number',
                                          'coerce': float}],
                                 choices={'type': {'category': _('Category'), 'event': _('Event')}},
                                 description=_("Specify categories/events shown in the 'upcoming events' list on the "
                                               "home page."))

    def validate_entries(self, field):
        if field.errors:
            return
        for entry in field.data:
            if entry['days'] < 0:
                raise ValidationError(_("'Days' must be a positive integer"))
            if entry['type'] not in {'category', 'event'}:
                raise ValidationError(_('Invalid type'))
            if entry['type'] == 'category' and not Category.get(entry['id'], is_deleted=False):
                raise ValidationError(_('Invalid category: {}').format(entry['id']))
            if entry['type'] == 'event' and not Event.get(entry['id'], is_deleted=False):
                raise ValidationError(_('Invalid event: {}').format(entry['id']))
