

from __future__ import absolute_import, unicode_literals

from fossir.core.db.sqlalchemy.colors import ColorTuple
from fossir.util.i18n import _
from fossir.web.forms.fields import JSONField
from fossir.web.forms.widgets import JinjaWidget


class fossirPalettePickerField(JSONField):
    """Field allowing user to pick a color from a set of predefined values"""

    widget = JinjaWidget('forms/palette_picker_widget.html')
    CAN_POPULATE = True

    def __init__(self, *args, **kwargs):
        self.color_list = kwargs.pop('color_list')
        super(fossirPalettePickerField, self).__init__(*args, **kwargs)

    def pre_validate(self, form):
        if self.data not in self.color_list:
            raise ValueError(_('Invalid colors selected'))

    def process_formdata(self, valuelist):
        super(fossirPalettePickerField, self).process_formdata(valuelist)
        self.data = ColorTuple(self.data['text'], self.data['background'])

    def process_data(self, value):
        super(fossirPalettePickerField, self).process_data(value)
        if self.object_data and self.object_data not in self.color_list:
            self.color_list = self.color_list + [self.object_data]

    def _value(self):
        return self.data._asdict()
