

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
