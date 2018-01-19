# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from fossir.core.db import db
from fossir.core.db.sqlalchemy.principals import PrincipalRolesMixin
from fossir.core.db.sqlalchemy.util.models import auto_table_args
from fossir.util.string import format_repr, return_ascii


class ContributionPrincipal(PrincipalRolesMixin, db.Model):
    __tablename__ = 'contribution_principals'
    principal_backref_name = 'in_contribution_acls'
    principal_for = 'Contribution'
    unique_columns = ('contribution_id',)
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
    #: The ID of the associated contribution
    contribution_id = db.Column(
        db.Integer,
        db.ForeignKey('events.contributions.id'),
        nullable=False,
        index=True
    )

    # relationship backrefs:
    # - contribution (Contribution.acl_entries)

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'id', 'contribution_id', 'principal', read_access=False, full_access=False, roles=[])
