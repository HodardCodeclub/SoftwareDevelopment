

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase


class WPLayoutEdit(WPEventManagement):
    template_prefix = 'events/layout/'
    sidemenu_option = 'layout'


class WPMenuEdit(WPEventManagement):
    template_prefix = 'events/layout/'
    sidemenu_option = 'menu'

    def getJSFiles(self):
        return WPEventManagement.getJSFiles(self) + self._asset_env['modules_event_layout_js'].urls()


class WPImages(WPEventManagement):
    template_prefix = 'events/layout/'
    sidemenu_option = 'images'


class WPPage(WPConferenceDisplayBase):
    template_prefix = 'events/layout/'

    def __init__(self, rh, conference, **kwargs):
        self.page = kwargs['page']
        WPConferenceDisplayBase.__init__(self, rh, conference, **kwargs)

    @property
    def sidemenu_option(self):
        return self.page.menu_entry.id
