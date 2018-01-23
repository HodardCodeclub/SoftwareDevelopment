

from __future__ import unicode_literals


def get_field_types():
    """Get a dict with all registration field types"""
    from .simple import (TextField, NumberField, TextAreaField, CheckboxField, DateField, BooleanField, PhoneField,
                         CountryField, FileField, EmailField)
    from .choices import SingleChoiceField, AccommodationField, MultiChoiceField
    return {field.name: field for field in (TextField, NumberField, TextAreaField, SingleChoiceField, CheckboxField,
                                            DateField, BooleanField, PhoneField, CountryField, FileField, EmailField,
                                            AccommodationField, MultiChoiceField)}
