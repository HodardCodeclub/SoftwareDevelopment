

from __future__ import unicode_literals

from datetime import timedelta

from wtforms.fields import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired

from fossir.modules.events.sessions.fields import SessionBlockPersonLinkListField
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import fossirForm
from fossir.web.forms.colors import get_colors
from fossir.web.forms.fields import (AccessControlListField, fossirLocationField, fossirPalettePickerField,
                                     fossirProtectionField, PrincipalListField, TimeDeltaField)
from fossir.web.forms.validators import UsedIf
from fossir.web.forms.widgets import SwitchWidget


class SessionForm(fossirForm):
    title = StringField(_('Title'), [DataRequired()])
    code = StringField(_('Session code'), description=_('The code that will identify the session in the Book of '
                                                        'Abstracts.'))
    description = TextAreaField(_('Description'))
    default_contribution_duration = TimeDeltaField(_('Default contribution duration'), units=('minutes', 'hours'),
                                                   description=_('Duration that a contribution created within this '
                                                                 'session will have by default.'),
                                                   default=timedelta(minutes=20))
    location_data = fossirLocationField(_("Default location"),
                                        description=_("Default location for blocks inside the session."))
    colors = fossirPalettePickerField(_('Colours'), color_list=get_colors())
    is_poster = BooleanField(_('Poster session'), widget=SwitchWidget(),
                             description=_('Whether the session is a poster session or contains normal presentations.'))

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        super(SessionForm, self).__init__(*args, **kwargs)
        if event.type != 'conference':
            del self.is_poster
            del self.code


class SessionProtectionForm(fossirForm):
    protection_mode = fossirProtectionField(_('Protection mode'), protected_object=lambda form: form.protected_object,
                                            acl_message_url=lambda form: url_for('sessions.acl_message',
                                                                                 form.protected_object))
    acl = AccessControlListField(_('Access control list'),
                                 [UsedIf(lambda form, field: form.protected_object.is_protected)],
                                 groups=True, allow_emails=True, default_text=_('Restrict access to this session'),
                                 description=_('List of users allowed to access the session.'))
    managers = PrincipalListField(_('Managers'), groups=True, allow_emails=True,
                                  description=_('List of users allowed to modify the session'))
    coordinators = PrincipalListField(_('Coordinators'), groups=True, allow_emails=True)

    def __init__(self, *args, **kwargs):
        self.protected_object = kwargs.pop('session')
        super(SessionProtectionForm, self).__init__(*args, **kwargs)


class SessionBlockForm(fossirForm):
    title = StringField(_('Title'), description=_('Title of the session block'))
    person_links = SessionBlockPersonLinkListField(_('Conveners'))
    location_data = fossirLocationField(_('Location'))

    def __init__(self, *args, **kwargs):
        self.session_block = kwargs.pop('session_block', None)
        super(SessionBlockForm, self).__init__(*args, **kwargs)


class MeetingSessionBlockForm(fossirForm):
    session_title = StringField(_('Title'), [DataRequired()], description=_('Title of the session'))
    block_title = StringField(_('Block title'), description=_('Title of the session block'))
    block_person_links = SessionBlockPersonLinkListField(_('Conveners'))
    block_location_data = fossirLocationField(_('Location'))

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        self.session_block = kwargs.pop('session_block', None)
        super(MeetingSessionBlockForm, self).__init__(*args, **kwargs)

    @property
    def session_fields(self):
        return [field_name for field_name in self._fields if field_name.startswith('session_')]

    @property
    def block_fields(self):
        return [field_name for field_name in self._fields if field_name.startswith('block_')]
