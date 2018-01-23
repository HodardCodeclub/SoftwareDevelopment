

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase, WPSimpleEventDisplayBase
from fossir.web.views import WPJinjaMixin


class WPManageSurvey(WPEventManagement):
    template_prefix = 'events/surveys/'
    sidemenu_option = 'surveys'

    def getJSFiles(self):
        return WPEventManagement.getJSFiles(self) + self._asset_env['modules_surveys_js'].urls()


class WPSurveyResults(WPManageSurvey):
    template_prefix = 'events/surveys/'

    def getCSSFiles(self):
        return (WPManageSurvey.getCSSFiles(self) +
                self._asset_env['chartist_css'].urls())

    def getJSFiles(self):
        return (WPManageSurvey.getJSFiles(self) +
                self._asset_env['chartist_js'].urls())


class DisplaySurveyMixin(WPJinjaMixin):
    template_prefix = 'events/surveys/'
    base_class = None

    def _getBody(self, params):
        return WPJinjaMixin._getPageContent(self, params)

    def getJSFiles(self):
        return self.base_class.getJSFiles(self) + self._asset_env['modules_surveys_js'].urls()


class WPDisplaySurveyConference(DisplaySurveyMixin, WPConferenceDisplayBase):
    template_prefix = 'events/surveys/'
    base_class = WPConferenceDisplayBase
    menu_entry_name = 'surveys'


class WPDisplaySurveySimpleEvent(DisplaySurveyMixin, WPSimpleEventDisplayBase):
    template_prefix = 'events/surveys/'
    base_class = WPSimpleEventDisplayBase
