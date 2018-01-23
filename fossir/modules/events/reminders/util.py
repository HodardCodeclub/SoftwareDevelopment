

from __future__ import unicode_literals

from fossir.modules.events.models.events import EventType
from fossir.web.flask.templating import get_template_module


def make_reminder_email(event, with_agenda, note):
    """Returns the template module for the reminder email.

    :param event: The event
    :param with_agenda: If the event's agenda should be included
    :param note: A custom message to include in the email
    """
    if event.type_ == EventType.lecture:
        with_agenda = False
    return get_template_module('events/reminders/emails/event_reminder.txt', event=event,
                               url=event.short_external_url, note=note, with_agenda=with_agenda,
                               agenda=event.timetable_entries.filter_by(parent_id=None))
