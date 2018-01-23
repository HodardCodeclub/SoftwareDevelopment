

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement


class WPManagePersons(WPEventManagement):
    template_prefix = 'events/persons/'
    sidemenu_option = 'persons'
