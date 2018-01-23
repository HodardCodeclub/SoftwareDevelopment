

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase, WPSimpleEventDisplayBase
from fossir.web.views import WPJinjaMixin


class WPAgreementFormSimpleEvent(WPJinjaMixin, WPSimpleEventDisplayBase):
    template_prefix = 'events/agreements/'

    def _getBody(self, params):
        return self._getPageContent(params)


class WPAgreementFormConference(WPConferenceDisplayBase):
    template_prefix = 'events/agreements/'


class WPAgreementManager(WPEventManagement):
    template_prefix = 'events/agreements/'
    sidemenu_option = 'agreements'
