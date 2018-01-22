

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin
from fossir.modules.users.views import WPUser


class WPAPIAdmin(WPAdmin):
    template_prefix = 'api/'
    sidemenu_option = 'api'


class WPAPIUserProfile(WPUser):
    template_prefix = 'api/'
