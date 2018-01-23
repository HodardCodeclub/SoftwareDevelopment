

from __future__ import unicode_literals

from marshmallow.fields import Raw, String
from marshmallow_sqlalchemy import column2field

from fossir.core.marshmallow import mm
from fossir.modules.events.contributions.models.fields import ContributionFieldValue
from fossir.modules.events.contributions.models.types import ContributionType


class ContributionTypeSchema(mm.ModelSchema):
    class Meta:
        model = ContributionType
        fields = ('id', 'name', 'description')


class ContributionFieldValueSchema(mm.Schema):
    id = column2field(ContributionFieldValue.contribution_field_id, attribute='contribution_field_id')
    name = String(attribute='contribution_field.title')
    value = Raw(attribute='friendly_data')

    class Meta:
        model = ContributionFieldValue
        fields = ('id', 'name', 'value')


contribution_type_schema = ContributionTypeSchema()
contribution_type_schema_basic = ContributionTypeSchema(only=('id', 'name'))
