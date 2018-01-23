

from __future__ import unicode_literals

from fossir.core.db import db
from fossir.core.db.sqlalchemy.util.models import get_simple_column_attrs
from fossir.core.db.sqlalchemy.util.session import no_autoflush
from fossir.modules.events.cloning import EventCloner
from fossir.modules.events.models.events import EventType
from fossir.modules.events.tracks.models.tracks import Track
from fossir.util.i18n import _


class TrackCloner(EventCloner):
    name = 'tracks'
    friendly_name = _('Tracks')
    always_available_dep = True

    @property
    def is_visible(self):
        return self.old_event.type_ == EventType.conference

    @property
    def is_available(self):
        return bool(self.old_event.tracks)

    @no_autoflush
    def run(self, new_event, cloners, shared_data):
        self._track_map = {}
        self._clone_tracks(new_event)
        db.session.flush()
        return {'track_map': self._track_map}

    def _clone_tracks(self, new_event):
        attrs = get_simple_column_attrs(Track) | {'abstract_reviewers', 'conveners'}
        for old_track in self.old_event.tracks:
            track = Track()
            track.populate_from_attrs(old_track, attrs)
            new_event.tracks.append(track)
            self._track_map[old_track] = track
