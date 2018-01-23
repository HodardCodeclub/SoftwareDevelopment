
from __future__ import unicode_literals

from fossir.modules.categories.views import WPCategoryManagement
from fossir.modules.events.management.views import WPEventManagement


class WPEventManagementDesigner(WPEventManagement):
    template_prefix = 'designer'

    def getJSFiles(self):
        return WPEventManagement.getJSFiles(self) + self._asset_env['modules_designer_js'].urls()


class WPCategoryManagementDesigner(WPCategoryManagement):
    template_prefix = 'designer'

    def getJSFiles(self):
        return WPCategoryManagement.getJSFiles(self) + self._asset_env['modules_designer_js'].urls()
