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

from fossir.modules.events.notes.models.notes import EventNote
from fossir.modules.events.notes.util import can_edit_note
from fossir.util.caching import memoize_request


class AttachedNotesMixin(object):
    """Allows for easy retrieval of structured information about
       items attached to the object"""
    # When set to ``True`` .has_note preload all notes that exist for the same event
    # Should be set to False when not applicable (no object.event property)
    PRELOAD_EVENT_NOTES = False

    @property
    @memoize_request
    def has_note(self):
        return EventNote.get_for_linked_object(self, preload_event=self.PRELOAD_EVENT_NOTES) is not None

    def can_edit_note(self, user):
        return can_edit_note(self, user)
