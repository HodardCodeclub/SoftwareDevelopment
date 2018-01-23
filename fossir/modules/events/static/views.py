

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement


class WPStaticSites(WPEventManagement):
    template_prefix = 'events/static/'
    sidemenu_option = 'static'
