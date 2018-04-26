

from __future__ import unicode_literals

from fossir.core import signals
from fossir.util.signals import named_objects_from_signal
from fossir.web.fields.base import BaseField


__all__ = ('BaseField', 'get_field_definitions')


def get_field_definitions(for_):
    """Gets a dict containing all field definitions

    :param for_: The identifier/object passed to the `get_fields`
                 signal to identify which fields to get.
    """
    return named_objects_from_signal(signals.get_fields.send(for_), plugin_attr='plugin')
