

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin
from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase


class WPPaymentAdmin(WPAdmin):
    template_prefix = 'events/payment/'


class WPPaymentEventManagement(WPEventManagement):
    template_prefix = 'events/payment/'
    sidemenu_option = 'payment'


class WPPaymentEvent(WPConferenceDisplayBase):
    template_prefix = 'events/payment/'
    menu_entry_name = 'registration'
