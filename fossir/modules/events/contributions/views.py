

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase
from fossir.util.mathjax import MathjaxMixin


class WPManageContributions(MathjaxMixin, WPEventManagement):
    template_prefix = 'events/contributions/'
    sidemenu_option = 'contributions'

    def getJSFiles(self):
        return (WPEventManagement.getJSFiles(self) +
                self._asset_env['modules_contributions_js'].urls() +
                self._asset_env['markdown_js'].urls())

    def _getHeadContent(self):
        return WPEventManagement._getHeadContent(self) + MathjaxMixin._getHeadContent(self)


class WPContributionsDisplayBase(WPConferenceDisplayBase):
    template_prefix = 'events/contributions/'

    def getJSFiles(self):
        return (WPConferenceDisplayBase.getJSFiles(self) +
                self._asset_env['modules_contributions_js'].urls() +
                self._asset_env['modules_event_display_js'].urls())


class WPMyContributions(WPContributionsDisplayBase):
    menu_entry_name = 'my_contributions'


class WPContributions(WPContributionsDisplayBase):
    menu_entry_name = 'contributions'

    def getJSFiles(self):
        return WPContributionsDisplayBase.getJSFiles(self) + self._asset_env['dropzone_js'].urls()

    def getCSSFiles(self):
        return WPContributionsDisplayBase.getCSSFiles(self) + self._asset_env['dropzone_css'].urls()


class WPAuthorList(WPContributionsDisplayBase):
    menu_entry_name = 'author_index'


class WPSpeakerList(WPContributionsDisplayBase):
    menu_entry_name = 'speaker_index'
