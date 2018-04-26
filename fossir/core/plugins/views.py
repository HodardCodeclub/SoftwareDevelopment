

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin


class WPPlugins(WPAdmin):
    template_prefix = 'plugins/'
    sidemenu_option = 'plugins'
