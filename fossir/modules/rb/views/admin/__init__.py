

from __future__ import unicode_literals

from flask import render_template

from fossir.modules.admin.views import WPAdmin


class WPRoomBookingAdminBase(WPAdmin):
    subtitle = u''

    def getJSFiles(self):
        return WPAdmin.getJSFiles(self) + self._includeJSPackage('Management')

    def _getPageContent(self, params):
        return render_template('rb/admin.html', body=self._get_legacy_content(params), subtitle=self.subtitle,
                               active_menu_item=self._kwargs['active_menu_item'])

    def _get_legacy_content(self, params):
        raise NotImplementedError
