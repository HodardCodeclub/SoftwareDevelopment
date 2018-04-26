

from __future__ import unicode_literals

from fossir.core.signals.event import _signals


person_updated = _signals.signal('person-updated', """
Called when an EventPerson is modified. The *sender* is the EventPerson.
""")
