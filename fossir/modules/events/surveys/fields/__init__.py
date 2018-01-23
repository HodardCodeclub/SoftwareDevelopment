

from __future__ import unicode_literals

from fossir.core import signals
from fossir.modules.events.surveys.fields.base import SurveyField
from fossir.web.fields import get_field_definitions


def get_field_types():
    """Gets a dict containing all field types"""
    return get_field_definitions(SurveyField)


@signals.get_fields.connect_via(SurveyField)
def _get_fields(sender, **kwargs):
    from .simple import SurveyTextField, SurveyNumberField, SurveyBoolField
    from .choices import SurveySingleChoiceField, SurveyMultiSelectField
    yield SurveyTextField
    yield SurveyNumberField
    yield SurveyBoolField
    yield SurveySingleChoiceField
    yield SurveyMultiSelectField


@signals.app_created.connect
def _check_field_definitions(app, **kwargs):
    # This will raise RuntimeError if the field names are not unique
    get_field_types()
