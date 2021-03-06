

from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from fossir.core.db import db
from fossir.core.db.sqlalchemy.principals import PrincipalRolesMixin
from fossir.core.db.sqlalchemy.util.models import auto_table_args
from fossir.util.string import format_repr, return_ascii


class EventPrincipal(PrincipalRolesMixin, db.Model):
    __tablename__ = 'principals'
    principal_backref_name = 'in_event_acls'
    principal_for = 'Event'
    unique_columns = ('event_id',)
    allow_emails = True
    allow_networks = True

    @declared_attr
    def __table_args__(cls):
        return auto_table_args(cls, schema='events')

    #: The ID of the acl entry
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #: The ID of the associated event
    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.events.id'),
        nullable=False,
        index=True
    )

    # relationship backrefs:
    # - event (Event.acl_entries)

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'id', 'event_id', 'principal', read_access=False, full_access=False, roles=[])
