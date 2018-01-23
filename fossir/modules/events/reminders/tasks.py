

from __future__ import unicode_literals

from celery.schedules import crontab

from fossir.core.celery import celery
from fossir.core.db import db
from fossir.modules.events import Event
from fossir.modules.events.reminders import logger
from fossir.modules.events.reminders.models.reminders import EventReminder
from fossir.util.date_time import now_utc


@celery.periodic_task(name='event_reminders', run_every=crontab(minute='*/5'))
def send_event_reminders():
    reminders = EventReminder.find_all(~EventReminder.is_sent, ~Event.is_deleted,
                                       EventReminder.scheduled_dt <= now_utc(),
                                       _join=EventReminder.event)
    for reminder in reminders:
        logger.info('Sending event reminder: %s', reminder)
        reminder.send()
    db.session.commit()
