

from __future__ import unicode_literals

from flask import request
from wtforms.fields import BooleanField, HiddenField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired

from fossir.modules.users.models.users import UserTitle
from fossir.util.i18n import _
from fossir.util.placeholders import render_placeholder_info
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import HiddenFieldList, fossirEmailRecipientsField, fossirEnumSelectField
from fossir.web.forms.widgets import CKEditorWidget, SwitchWidget


class EmailEventPersonsForm(fossirForm):
    from_address = SelectField(_('From'), [DataRequired()])
    subject = StringField(_('Subject'), [DataRequired()])
    body = TextAreaField(_('Email body'), [DataRequired()], widget=CKEditorWidget(simple=True))
    recipients = fossirEmailRecipientsField(_('Recipients'))
    copy_for_sender = BooleanField(_('Send copy to me'), widget=SwitchWidget(),
                                   description=_('Send copy of each email to my mailbox'))
    person_id = HiddenFieldList()
    user_id = HiddenFieldList()
    submitted = HiddenField()

    def __init__(self, *args, **kwargs):
        register_link = kwargs.pop('register_link')
        event = kwargs.pop('event')
        super(EmailEventPersonsForm, self).__init__(*args, **kwargs)
        self.from_address.choices = event.get_allowed_sender_emails().items()
        self.body.description = render_placeholder_info('event-persons-email', event=None, person=None,
                                                        register_link=register_link)

    def is_submitted(self):
        return super(EmailEventPersonsForm, self).is_submitted() and 'submitted' in request.form


class EventPersonForm(fossirForm):
    title = fossirEnumSelectField(_('Title'), enum=UserTitle)
    first_name = StringField(_('First name'), [DataRequired()])
    last_name = StringField(_('Family name'), [DataRequired()])
    affiliation = StringField(_('Affiliation'))
    address = TextAreaField(_('Address'))
    phone = StringField(_('Phone number'))
