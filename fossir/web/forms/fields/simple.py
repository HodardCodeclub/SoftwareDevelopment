

from __future__ import absolute_import, unicode_literals

import json

from markupsafe import escape
from wtforms.fields import Field, HiddenField, PasswordField, RadioField, SelectMultipleField, TextAreaField
from wtforms.widgets import CheckboxInput

from fossir.util.i18n import _
from fossir.util.string import is_valid_mail, sanitize_email
from fossir.web.forms.fields.util import is_preprocessed_formdata
from fossir.web.forms.widgets import HiddenInputs, JinjaWidget, PasswordWidget


class fossirSelectMultipleCheckboxField(SelectMultipleField):
    widget = JinjaWidget('forms/checkbox_group_widget.html', single_kwargs=True)
    option_widget = CheckboxInput()


class fossirSelectMultipleCheckboxBooleanField(fossirSelectMultipleCheckboxField):
    def process_formdata(self, valuelist):
        super(fossirSelectMultipleCheckboxBooleanField, self).process_formdata(valuelist)
        values = set(self.data)
        self.data = {x[0]: x[0] in values for x in self.choices}

    def iter_choices(self):
        for value, label in self.choices:
            selected = self.data is not None and self.data.get(self.coerce(value))
            yield (value, label, selected)


class fossirRadioField(RadioField):
    widget = JinjaWidget('forms/radio_buttons_widget.html', single_kwargs=True)

    def __init__(self, *args, **kwargs):
        self.option_orientation = kwargs.pop('orientation', 'vertical')
        super(fossirRadioField, self).__init__(*args, **kwargs)


class JSONField(HiddenField):
    #: Whether an object may be populated with the data from this field
    CAN_POPULATE = False

    def process_formdata(self, valuelist):
        if is_preprocessed_formdata(valuelist):
            self.data = valuelist[0]
        elif valuelist:
            self.data = json.loads(valuelist[0])

    def _value(self):
        return json.dumps(self.data)

    def populate_obj(self, obj, name):
        if self.CAN_POPULATE:
            super(JSONField, self).populate_obj(obj, name)


class HiddenFieldList(HiddenField):
    """A hidden field that handles lists of strings.

    This is done `getlist`-style, i.e. by repeating the input element
    with the same name for each list item.

    The only case where this field is useful is when you display a
    form via POST and provide a list of items (e.g. ids) related
    to the form which needs to be kept when the form is submitted and
    also need to access it via ``request.form.getlist(...)`` before
    submitting the form.
    """

    widget = HiddenInputs()

    def process_formdata(self, valuelist):
        self.data = valuelist

    def _value(self):
        return self.data


class TextListField(TextAreaField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [line.strip() for line in valuelist[0].split('\n') if line.strip()]
        else:
            self.data = []

    def _validate_item(self, line):
        pass

    def pre_validate(self, form):
        for line in self.data:
            self._validate_item(line)

    def _value(self):
        return '\n'.join(self.data) if self.data else ''


class EmailListField(TextListField):
    def process_formdata(self, valuelist):
        super(EmailListField, self).process_formdata(valuelist)
        self.data = map(sanitize_email, self.data)

    def _validate_item(self, line):
        if not is_valid_mail(line, False):
            raise ValueError(_('Invalid email address: {}').format(escape(line)))


class fossirPasswordField(PasswordField):
    """Password field which can show or hide the password."""

    widget = PasswordWidget()

    def __init__(self, *args, **kwargs):
        self.toggle = kwargs.pop('toggle', False)
        super(fossirPasswordField, self).__init__(*args, **kwargs)


class fossirStaticTextField(Field):
    """Return an html element with text taken from this field's value"""

    widget = JinjaWidget('forms/static_text_widget.html')

    def __init__(self, *args, **kwargs):
        self.text_value = kwargs.pop('text', '')
        super(fossirStaticTextField, self).__init__(*args, **kwargs)

    def process_data(self, data):
        self.text_value = self.data = unicode(data)

    def _value(self):
        return self.text_value


class fossirEmailRecipientsField(Field):
    widget = JinjaWidget('forms/email_recipients_widget.html', single_kwargs=True)

    def process_data(self, data):
        self.data = sorted(data, key=unicode.lower)
        self.text_value = ', '.join(data)
        self.count = len(data)


class fossirTagListField(HiddenFieldList):
    widget = JinjaWidget('forms/tag_list_widget.html', single_kwargs=True)
