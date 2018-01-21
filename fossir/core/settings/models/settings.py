.

from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from fossir.core.db.sqlalchemy import db
from fossir.core.db.sqlalchemy.util.models import auto_table_args
from fossir.core.settings.models.base import JSONSettingsBase, PrincipalSettingsBase
from fossir.util.decorators import strict_classproperty
from fossir.util.string import return_ascii


class CoreSettingsMixin(object):
    @strict_classproperty
    @staticmethod
    def __auto_table_args():
        return (db.Index(None, 'module', 'name'),
                {'schema': 'fossir'})


class Setting(JSONSettingsBase, CoreSettingsMixin, db.Model):
    @strict_classproperty
    @staticmethod
    def __auto_table_args():
        return db.UniqueConstraint('module', 'name'),

    @declared_attr
    def __table_args__(cls):
        return auto_table_args(cls)

    @return_ascii
    def __repr__(self):
        return '<Setting({}, {}, {!r})>'.format(self.module, self.name, self.value)


class SettingPrincipal(PrincipalSettingsBase, CoreSettingsMixin, db.Model):
    principal_backref_name = 'in_settings_acls'

    @declared_attr
    def __table_args__(cls):
        return auto_table_args(cls)

    @return_ascii
    def __repr__(self):
        return '<SettingPrincipal({}, {}, {!r})>'.format(self.module, self.name, self.principal)
