

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement


class WPEventLogs(WPEventManagement):
    template_prefix = 'events/logs/'
    sidemenu_option = 'logs'
