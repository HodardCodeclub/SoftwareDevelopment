

from __future__ import unicode_literals

from wtforms.fields.core import BooleanField, IntegerField, StringField
from wtforms.validators import InputRequired, NumberRange

from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import EmailListField, PrincipalListField


GOOGLE_API_KEY_DOCS = 'https://developers.google.com/maps/documentation/javascript/get-api-key'
GOOGLE_API_KEY_DESC = _('When using the "map of rooms" widget, you need to register a '
                        '<a href="{link}">Google Maps API key</a>.').format(link=GOOGLE_API_KEY_DOCS)


class SettingsForm(fossirForm):
    admin_principals = PrincipalListField(_('Administrators'), groups=True)
    authorized_principals = PrincipalListField(_('Authorized users/groups'), groups=True)
    assistance_emails = EmailListField(_('Assistance email addresses (one per line)'))
    notification_before_days = IntegerField(_('Send booking reminders X days before (single/daily)'),
                                            [InputRequired(), NumberRange(min=1, max=30)])
    notification_before_days_weekly = IntegerField(_('Send booking reminders X days before (weekly)'),
                                                   [InputRequired(), NumberRange(min=1, max=30)])
    notification_before_days_monthly = IntegerField(_('Send booking reminders X days before (monthly)'),
                                                    [InputRequired(), NumberRange(min=1, max=30)])
    notifications_enabled = BooleanField(_('Reminders enabled'))
    vc_support_emails = EmailListField(_('Videoconference support email addresses (one per line)'))
    booking_limit = IntegerField(_('Maximum length of booking (days)'), [InputRequired(), NumberRange(min=1)])
    google_maps_api_key = StringField(_('Google Maps API key'), description=GOOGLE_API_KEY_DESC)
