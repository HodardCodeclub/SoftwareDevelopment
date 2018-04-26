

from __future__ import absolute_import, unicode_literals

from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import CheckboxInput

from fossir.web.forms.widgets import JinjaWidget


class fossirQuerySelectMultipleField(QuerySelectMultipleField):
    """Like the parent, but with a callback that allows you to modify the list

    The callback can return a new list or yield items, and you can use it e.g. to sort the list.
    """

    def __init__(self, *args, **kwargs):
        self.modify_object_list = kwargs.pop('modify_object_list', None)
        self.collection_class = kwargs.pop('collection_class', list)
        super(fossirQuerySelectMultipleField, self).__init__(*args, **kwargs)

    def _get_object_list(self):
        object_list = super(fossirQuerySelectMultipleField, self)._get_object_list()
        if self.modify_object_list:
            object_list = list(self.modify_object_list(object_list))
        return object_list

    def _get_data(self):
        data = super(fossirQuerySelectMultipleField, self)._get_data()
        return self.collection_class(data)

    data = property(_get_data, QuerySelectMultipleField._set_data)


class fossirQuerySelectMultipleCheckboxField(fossirQuerySelectMultipleField):
    option_widget = CheckboxInput()
    widget = JinjaWidget('forms/checkbox_group_widget.html', single_kwargs=True)
