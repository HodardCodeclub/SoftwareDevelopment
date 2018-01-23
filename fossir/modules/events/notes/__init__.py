

from __future__ import unicode_literals

from fossir.core import signals
from fossir.core.logger import Logger


logger = Logger.get('events.notes')


@signals.users.merged.connect
def _merge_users(target, source, **kwargs):
    from fossir.modules.events.notes.models.notes import EventNoteRevision
    EventNoteRevision.find(user_id=source.id).update({EventNoteRevision.user_id: target.id})


@signals.event_management.get_cloners.connect
def _get_attachment_cloner(sender, **kwargs):
    from fossir.modules.events.notes.clone import NoteCloner
    return NoteCloner
