

from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from fossir.core.db import db
from fossir.core.db.sqlalchemy.principals import PrincipalRolesMixin
from fossir.core.db.sqlalchemy.util.models import auto_table_args
from fossir.util.string import format_repr, return_ascii


class CategoryPrincipal(PrincipalRolesMixin, db.Model):
    __tablename__ = 'principals'
    principal_backref_name = 'in_category_acls'
    principal_for = 'Category'
    unique_columns = ('category_id',)
    allow_networks = True

    @declared_attr
    def __table_args__(cls):
        return auto_table_args(cls, schema='categories')

    #: The ID of the acl entry
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #: The ID of the associated event
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.categories.id'),
        nullable=False,
        index=True
    )

    # relationship backrefs:
    # - category (Category.acl_entries)

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'id', 'category_id', 'principal', read_access=False, full_access=False, roles=[])
