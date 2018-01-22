

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin
from fossir.util.i18n import _
from fossir.web.breadcrumbs import render_breadcrumbs
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPSettings(WPAdmin):
    template_prefix = 'core/'

    def getJSFiles(self):
        return WPAdmin.getJSFiles(self) + self._asset_env['modules_cephalopod_js'].urls()


class WPContact(WPJinjaMixin, WPDecorated):
    template_prefix = 'core/'

    def _get_breadcrumbs(self):
        return render_breadcrumbs(_('Contact'))

    def _getBody(self, params):
        return self._getPageContent(params)
