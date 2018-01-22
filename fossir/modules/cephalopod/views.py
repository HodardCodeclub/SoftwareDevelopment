

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin


class WPCephalopod(WPAdmin):
    template_prefix = 'cephalopod/'

    def getJSFiles(self):
        return WPAdmin.getJSFiles(self) + self._asset_env['modules_cephalopod_js'].urls()
