

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement


class WPReminders(WPEventManagement):
    template_prefix = 'events/reminders/'
    sidemenu_option = 'reminders'
