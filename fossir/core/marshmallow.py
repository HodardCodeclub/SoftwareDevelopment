

from __future__ import absolute_import, unicode_literals

from inspect import getmro

from flask_marshmallow import Marshmallow
from flask_marshmallow.sqla import SchemaOpts
from marshmallow import fields
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelConverter
from sqlalchemy.orm import ColumnProperty

from fossir.core.db.sqlalchemy import PyIntEnum, UTCDateTime


mm = Marshmallow()


class fossirModelConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        UTCDateTime: fields.DateTime,
        PyIntEnum: EnumField
    })

    def _get_field_kwargs_for_property(self, prop):
        kwargs = super(fossirModelConverter, self)._get_field_kwargs_for_property(prop)
        if isinstance(prop, ColumnProperty) and hasattr(prop.columns[0].type, 'marshmallow_get_field_kwargs'):
            kwargs.update(prop.columns[0].type.marshmallow_get_field_kwargs())
        return kwargs

    def fields_for_model(self, model, *args, **kwargs):
        # Look up aliases on all classes in the inheritance chain of
        # the model so mixins can define their own aliases if needed.
        def _get_from_mro(attr, key, default=None, _mro=getmro(model)):
            for cls in _mro:
                try:
                    return getattr(cls, attr, {})[key]
                except (TypeError, KeyError, AttributeError):
                    continue
            return default

        # XXX: To allow renaming/aliasing of fields we need to let mm-sqlalchemy
        # generate all fields from the models and leave it up to mm itself to
        # exclude fields we don't care about
        kwargs['fields'] = ()
        fields = super(fossirModelConverter, self).fields_for_model(model, *args, **kwargs)
        for key, field in fields.items():
            new_key = _get_from_mro('marshmallow_aliases', key)
            if new_key:
                del fields[key]
                fields[new_key] = field
                if field.attribute is None:
                    field.attribute = key
        return fields


class _fossirSchemaOpts(SchemaOpts):
    def __init__(self, meta):
        super(_fossirSchemaOpts, self).__init__(meta)
        self.model_converter = getattr(meta, 'model_converter', fossirModelConverter)


class fossirModelSchema(mm.ModelSchema):
    OPTIONS_CLASS = _fossirSchemaOpts


mm.ModelSchema = fossirModelSchema
