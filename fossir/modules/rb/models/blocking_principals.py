

from __future__ import unicode_literals

from fossir.core.db import db
from fossir.core.db.sqlalchemy.principals import PrincipalMixin
from fossir.util.string import return_ascii


class BlockingPrincipal(PrincipalMixin, db.Model):
    __tablename__ = 'blocking_principals'
    __table_args__ = {'schema': 'roombooking'}
    principal_backref_name = 'in_blocking_acls'
    unique_columns = ('blocking_id',)

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    blocking_id = db.Column(
        db.Integer,
        db.ForeignKey('roombooking.blockings.id'),
        nullable=False
    )

    # relationship backrefs:
    # - blocking (Blocking._allowed)

    @return_ascii
    def __repr__(self):
        return '<BlockingPrincipal({}, {}, {})>'.format(
            self.id,
            self.blocking_id,
            self.principal
        )
