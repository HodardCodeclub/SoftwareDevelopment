

from __future__ import unicode_literals

from wtforms.fields import BooleanField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.validators import fossirRegexp
from fossir.web.forms.widgets import SwitchWidget


class ReportErrorForm(fossirForm):
    comment = TextAreaField(_('Details'), [DataRequired()], render_kw={'rows': 5},
                            description=_('Please let us know what you were doing when the error showed up.'))
    email = EmailField(_('Email address'),
                       description=_('If you enter your email address we can contact you to follow-up '
                                     'on your error report.'))


class SettingsForm(fossirForm):
    # Core settings
    core_site_title = StringField(_('Title'), [DataRequired()], description=_("The global title of this fossir site."))
    core_site_organization = StringField(_('Organization'),
                                         description=_("The organization that runs this fossir site."))

    # Social settings
    social_enabled = BooleanField(_('Enabled'), widget=SwitchWidget())
    social_facebook_app_id = StringField('Facebook App ID', [fossirRegexp(r'^\d*$')])

    @property
    def _fieldsets(self):
        return [
            (_('Site'), [x for x in self._fields if x.startswith('core_')]),
            (_('Social'), [x for x in self._fields if x.startswith('social_')]),
        ]
