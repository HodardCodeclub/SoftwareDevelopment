# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin
from fossir.util.i18n import _
from fossir.web.breadcrumbs import render_breadcrumbs
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPSettings(WPAdmin):
    template_prefix = 'core/'

    def getJSFiles(self):
        return WPAdmin.getJSFiles(self) + self._asset_env['modules_cephalopod_js'].urls()


class WPContact(WPJinjaMixin, WPDecorated):
    template_prefix = 'core/'

    def _get_breadcrumbs(self):
        return render_breadcrumbs(_('Contact'))

    def _getBody(self, params):
        return self._getPageContent(params)