

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement


class WPRequestsEventManagement(WPEventManagement):
    sidemenu_option = 'requests'
