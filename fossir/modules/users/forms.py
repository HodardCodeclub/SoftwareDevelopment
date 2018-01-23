

from __future__ import unicode_literals

from operator import itemgetter

from pytz import common_timezones, common_timezones_set
from wtforms.fields.core import BooleanField, SelectField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, ValidationError

from fossir.core.config import config
from fossir.modules.auth.forms import LocalRegistrationForm, _check_existing_email
from fossir.modules.users import User
from fossir.modules.users.models.emails import UserEmail
from fossir.modules.users.models.users import NameFormat, UserTitle
from fossir.util.i18n import _, get_all_locales
from fossir.web.forms.base import fossirForm, SyncedInputsMixin
from fossir.web.forms.fields import fossirEnumSelectField, PrincipalField, PrincipalListField
from fossir.web.forms.util import inject_validators
from fossir.web.forms.validators import HiddenUnless, used_if_not_synced
from fossir.web.forms.widgets import SwitchWidget, SyncedInputWidget


class UserDetailsForm(SyncedInputsMixin, fossirForm):
    title = fossirEnumSelectField(_('Title'), enum=UserTitle)
    first_name = StringField(_('First name'), [used_if_not_synced, DataRequired()], widget=SyncedInputWidget())
    last_name = StringField(_('Family name'), [used_if_not_synced, DataRequired()], widget=SyncedInputWidget())
    affiliation = StringField(_('Affiliation'), widget=SyncedInputWidget())
    address = TextAreaField(_('Address'), widget=SyncedInputWidget(textarea=True))
    phone = StringField(_('Phone number'), widget=SyncedInputWidget())


class UserPreferencesForm(fossirForm):
    lang = SelectField(_('Language'))
    timezone = SelectField(_('Timezone'))

    force_timezone = BooleanField(
        _('Use my timezone'),
        widget=SwitchWidget(),
        description=_("Always use my current timezone instead of an event's timezone."))

    show_past_events = BooleanField(
        _('Show past events'),
        widget=SwitchWidget(),
        description=_('Show past events by default.'))

    name_format = fossirEnumSelectField(_('Name format'), enum=NameFormat,
                                        description=_('Default format in which names are displayed'))

    use_previewer_pdf = BooleanField(
        _('Use previewer for PDF files'),
        widget=SwitchWidget(),
        description=_('The previewer is used by default for image and text files, but not for PDF files.'))

    def __init__(self, *args, **kwargs):
        super(UserPreferencesForm, self).__init__(*args, **kwargs)
        self.lang.choices = sorted(get_all_locales().items(), key=itemgetter(1))
        self.timezone.choices = zip(common_timezones, common_timezones)
        if self.timezone.object_data and self.timezone.object_data not in common_timezones_set:
            self.timezone.choices.append((self.timezone.object_data, self.timezone.object_data))


class UserEmailsForm(fossirForm):
    email = EmailField(_('Add new email address'), [DataRequired()], filters=[lambda x: x.lower() if x else x])

    def validate_email(self, field):
        if UserEmail.find(~User.is_pending, is_user_deleted=False, email=field.data, _join=User).count():
            raise ValidationError(_('This email address is already in use.'))


class SearchForm(fossirForm):
    last_name = StringField(_('Family name'))
    first_name = StringField(_('First name'))
    email = StringField(_('Email'), filters=[lambda x: x.lower() if x else x])
    affiliation = StringField(_('Affiliation'))
    exact = BooleanField(_('Exact match'))
    include_deleted = BooleanField(_('Include deleted'))
    include_pending = BooleanField(_('Include pending'))
    external = BooleanField(_('External'))


class MergeForm(fossirForm):
    source_user = PrincipalField(_('Source user'), [DataRequired()],
                                 description=_('The user that will be merged into the target one'))
    target_user = PrincipalField(_('Target user'), [DataRequired()],
                                 description=_('The user that will remain active in the end'))


class AdminUserSettingsForm(fossirForm):
    notify_account_creation = BooleanField(_('Registration notifications'), widget=SwitchWidget(),
                                           description=_('Send an email to all administrators whenever someone '
                                                         'registers a new local account.'))


class AdminAccountRegistrationForm(LocalRegistrationForm):
    email = EmailField(_('Email address'), [DataRequired(), _check_existing_email])
    create_identity = BooleanField(_("Set login details"), widget=SwitchWidget(), default=True)

    def __init__(self, *args, **kwargs):
        if config.LOCAL_IDENTITIES:
            for field in ('username', 'password', 'confirm_password'):
                inject_validators(self, field, [HiddenUnless('create_identity')], early=True)
        super(AdminAccountRegistrationForm, self).__init__(*args, **kwargs)
        del self.comment
        if not config.LOCAL_IDENTITIES:
            del self.username
            del self.password
            del self.confirm_password
            del self.create_identity


class AdminsForm(fossirForm):
    admins = PrincipalListField(_('Admins'), [DataRequired()])
