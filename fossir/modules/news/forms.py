

from __future__ import unicode_literals

from wtforms.fields import BooleanField, IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, NumberRange

from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.validators import HiddenUnless
from fossir.web.forms.widgets import CKEditorWidget, SwitchWidget


class NewsSettingsForm(fossirForm):
    show_recent = BooleanField('Show headlines', widget=SwitchWidget(),
                               description=_('Whether to show the latest news headlines on the fossir home page.'))
    max_entries = IntegerField(_('Max. headlines'), [HiddenUnless('show_recent'), DataRequired(), NumberRange(min=1)],
                               description=_("The maximum number of news headlines to show on the fossir home page."))
    max_age = IntegerField(_('Max. age'), [HiddenUnless('show_recent'), InputRequired(), NumberRange(min=0)],
                           description=_("The maximum age in days for news to show up on the fossir home page. "
                                         "Setting it to 0 will show news no matter how old they are."))
    new_days = IntegerField(_('"New" threshold'), [InputRequired(), NumberRange(min=0)],
                            description=_('The maximum age in days for news to be considered "new". Setting it to 0 '
                                          'will disable the "new" label altogether.'))


class NewsForm(fossirForm):
    title = StringField(_('Title'), [DataRequired()])
    content = TextAreaField(_('Content'), [DataRequired()], widget=CKEditorWidget())
