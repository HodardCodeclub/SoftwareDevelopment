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

from fossir.core.db.sqlalchemy import PyIntEnum, db
from fossir.modules.events.contributions.models.persons import AuthorType
from fossir.modules.events.models.persons import PersonLinkBase
from fossir.util.locators import locator_property
from fossir.util.string import format_repr, return_ascii


class AbstractPersonLink(PersonLinkBase):
    """Association between EventPerson and Abstract."""

    __tablename__ = 'abstract_person_links'
    __auto_table_args = {'schema': 'event_abstracts'}
    person_link_backref_name = 'abstract_links'
    person_link_unique_columns = ('abstract_id',)
    object_relationship_name = 'abstract'

    abstract_id = db.Column(
        db.Integer,
        db.ForeignKey('event_abstracts.abstracts.id'),
        index=True,
        nullable=False
    )
    is_speaker = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    author_type = db.Column(
        PyIntEnum(AuthorType),
        nullable=False,
        default=AuthorType.none
    )

    # relationship backrefs:
    # - abstract (Abstract.person_links)

    @locator_property
    def locator(self):
        return dict(self.abstract.locator, person_id=self.id)

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'id', 'person_id', 'abstract_id', is_speaker=False, author_type=None,
                           _text=self.full_name)
