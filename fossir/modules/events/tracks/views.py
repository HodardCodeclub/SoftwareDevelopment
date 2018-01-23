

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase
from fossir.util.mathjax import MathjaxMixin


class WPManageTracks(MathjaxMixin, WPEventManagement):
    template_prefix = 'events/tracks/'
    sidemenu_option = 'program'

    def getJSFiles(self):
        return (WPEventManagement.getJSFiles(self) +
                self._asset_env['markdown_js'].urls() +
                self._asset_env['modules_tracks_js'].urls())

    def _getHeadContent(self):
        return WPEventManagement._getHeadContent(self) + MathjaxMixin._getHeadContent(self)


class WPDisplayTracks(WPConferenceDisplayBase):
    template_prefix = 'events/tracks/'
    menu_entry_name = 'program'

    def getJSFiles(self):
        return (WPConferenceDisplayBase.getJSFiles(self) +
                self._asset_env['markdown_js'].urls() +
                self._asset_env['modules_tracks_js'].urls())
