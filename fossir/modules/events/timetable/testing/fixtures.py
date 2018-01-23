

from __future__ import unicode_literals

import pytest

from fossir.modules.events.timetable.models.entries import TimetableEntry


@pytest.fixture
def create_entry(db, dummy_event):
    """Returns a a callable which lets you create timetable"""

    def _create_entry(obj, start_dt):
        entry = TimetableEntry(event=dummy_event, object=obj, start_dt=start_dt)
        db.session.add(entry)
        db.session.flush()
        return entry

    return _create_entry
