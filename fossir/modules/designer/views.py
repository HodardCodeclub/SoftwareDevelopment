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
