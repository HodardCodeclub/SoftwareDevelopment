

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin
from fossir.util.i18n import _
from fossir.web.breadcrumbs import render_breadcrumbs
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPLegalMixin:
    template_prefix = 'legal/'


class WPManageLegalMessages(WPLegalMixin, WPAdmin):
    pass


class WPDisplayLegalMessages(WPLegalMixin, WPJinjaMixin, WPDecorated):
    def _get_breadcrumbs(self):
        return render_breadcrumbs(_('Terms and Conditions'))

    def _getBody(self, params):
        return self._getPageContent(params)
