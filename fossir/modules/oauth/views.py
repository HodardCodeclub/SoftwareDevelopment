# This file is part of Indico.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from indico.modules.admin.views import WPAdmin
from indico.modules.users.views import WPUser
from indico.web.views import WPJinjaMixin


class WPOAuthJinjaMixin(WPJinjaMixin):
    template_prefix = 'oauth/'


class WPOAuthAdmin(WPOAuthJinjaMixin, WPAdmin):
    sidemenu_option = 'applications'


class WPOAuthUserProfile(WPOAuthJinjaMixin, WPUser):
    pass