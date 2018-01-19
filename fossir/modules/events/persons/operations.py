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

from flask import session

from fossir.core import signals
from fossir.core.db import db
from fossir.modules.events.logs import EventLogKind, EventLogRealm
from fossir.modules.events.persons import logger


def update_person(person, data):
    person.populate_from_dict(data)
    db.session.flush()
    signals.event.person_updated.send(person)
    logger.info('Person %s updated by %s', person, session.user)
    person.event.log(EventLogRealm.management, EventLogKind.change, 'Persons',
                     "Person with email '{}' has been updated".format(person.email), session.user)
