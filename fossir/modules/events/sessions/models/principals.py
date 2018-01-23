

from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from fossir.core.db import db
from fossir.core.db.sqlalchemy.principals import PrincipalRolesMixin
from fossir.core.db.sqlalchemy.util.models import auto_table_args
from fossir.util.string import format_repr, return_ascii


class SessionPrincipal(PrincipalRolesMixin, db.Model):
    __tablename__ = 'session_principals'
    principal_backref_name = 'in_session_acls'
    principal_for = 'Session'
    unique_columns = ('session_id',)
    disallowed_protection_modes = frozenset()
    allow_emails = True

    @declared_attr
    def __table_args__(cls):
        return auto_table_args(cls, schema='events')

    #: The ID of the acl entry
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #: The ID of the associated session
    session_id = db.Column(
        db.Integer,
        db.ForeignKey('events.sessions.id'),
        nullable=False,
        index=True
    )

    # relationship backrefs:
    # - session (Session.acl_entries)

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'id', 'session_id', 'principal', read_access=False, full_access=False, roles=[])
