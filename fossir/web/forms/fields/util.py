

from __future__ import absolute_import, unicode_literals


def is_preprocessed_formdata(valuelist):
    if len(valuelist) != 1:
        return False
    value = valuelist[0]
    return isinstance(value, (dict, list))
