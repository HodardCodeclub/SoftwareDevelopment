

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin
from fossir.modules.users.views import WPUser
from fossir.web.views import WPJinjaMixin


class WPOAuthJinjaMixin(WPJinjaMixin):
    template_prefix = 'oauth/'


class WPOAuthAdmin(WPOAuthJinjaMixin, WPAdmin):
    sidemenu_option = 'applications'


class WPOAuthUserProfile(WPOAuthJinjaMixin, WPUser):
    pass
