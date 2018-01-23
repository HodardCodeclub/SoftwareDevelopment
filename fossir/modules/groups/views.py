

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin


class WPGroupsAdmin(WPAdmin):
    template_prefix = 'groups/'
    sidemenu_option = 'groups'
