

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase


class WPManageSessions(WPEventManagement):
    template_prefix = 'events/sessions/'
    sidemenu_option = 'sessions'

    def getJSFiles(self):
        return WPEventManagement.getJSFiles(self) + self._asset_env['modules_sessions_js'].urls()


class WPDisplaySession(WPConferenceDisplayBase):
    template_prefix = 'events/sessions/'
    menu_entry_name = 'timetable'

    def getJSFiles(self):
        return WPConferenceDisplayBase.getJSFiles(self) + self._asset_env['modules_timetable_js'].urls()


class WPDisplayMySessionsConference(WPDisplaySession):
    menu_entry_name = 'my_sessions'
