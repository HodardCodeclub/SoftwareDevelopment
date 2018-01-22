

from __future__ import unicode_literals

from fossir.modules.users.views import WPUser
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPAuth(WPJinjaMixin, WPDecorated):
    template_prefix = 'auth/'

    def _getBody(self, params):
        return self._getPageContent(params)


class WPAuthUser(WPUser):
    template_prefix = 'auth/'
