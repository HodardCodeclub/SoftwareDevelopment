

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin
from fossir.util.i18n import _
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPNews(WPJinjaMixin, WPDecorated):
    template_prefix = 'news/'
    title = _('News')

    def _getBody(self, params):
        return self._getPageContent(params)


class WPManageNews(WPAdmin):
    template_prefix = 'news/'
