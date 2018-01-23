

from __future__ import unicode_literals

from fossir.modules.events.logs.models.entries import EventLogEntry
from fossir.modules.events.logs.views import WPEventLogs
from fossir.modules.events.management.controllers import RHManageEventBase


class RHEventLogs(RHManageEventBase):
    """Shows the modification/action log for the event"""

    def _process(self):
        entries = self.event.log_entries.order_by(EventLogEntry.logged_dt.desc()).all()
        realms = {e.realm for e in entries}
        return WPEventLogs.render_template('logs.html', self.event, entries=entries, realms=realms)
