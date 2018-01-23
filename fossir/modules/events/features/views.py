

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement


class WPFeatures(WPEventManagement):
    template_prefix = 'events/features/'
    sidemenu_option = 'features'
