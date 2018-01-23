

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase
from fossir.util.i18n import _
from fossir.web.breadcrumbs import render_breadcrumbs
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPVCManageEvent(WPEventManagement):
    sidemenu_option = 'videoconference'
    template_prefix = 'vc/'

    def getCSSFiles(self):
        return WPEventManagement.getCSSFiles(self) + self._asset_env['selectize_css'].urls()

    def getJSFiles(self):
        return (WPEventManagement.getJSFiles(self) +
                self._asset_env['modules_vc_js'].urls() +
                self._asset_env['selectize_js'].urls())


class WPVCEventPage(WPConferenceDisplayBase):
    menu_entry_name = 'videoconference_rooms'
    template_prefix = 'vc/'

    def getJSFiles(self):
        return WPConferenceDisplayBase.getJSFiles(self) + self._asset_env['modules_vc_js'].urls()


class WPVCService(WPJinjaMixin, WPDecorated):
    template_prefix = 'vc/'

    def _get_breadcrumbs(self):
        return render_breadcrumbs(_('Videoconference'))

    def _getBody(self, params):
        return self._getPageContent(params)
