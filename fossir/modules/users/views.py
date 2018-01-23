

from __future__ import unicode_literals

from flask import request

from fossir.modules.admin.views import WPAdmin
from fossir.modules.users import User
from fossir.util.i18n import _
from fossir.web.breadcrumbs import render_breadcrumbs
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPUser(WPJinjaMixin, WPDecorated):
    """Base WP for user profile pages.

    Whenever you use this, you MUST include `user` in the params passed to
    `render_template`. Any RH using this should inherit from `RHUserBase`
    which already handles user/admin access. In this case, simply add
    ``user=self.user`` to your `render_template` call.
    """

    template_prefix = 'users/'

    def __init__(self, rh, active_menu_item, **kwargs):
        kwargs['active_menu_item'] = active_menu_item
        WPDecorated.__init__(self, rh, **kwargs)

    def _get_breadcrumbs(self):
        if 'user_id' in request.view_args:
            user = User.get(request.view_args['user_id'])
            profile_breadcrumb = _('Profile of {name}').format(name=user.full_name)
        else:
            profile_breadcrumb = _('My Profile')
        return render_breadcrumbs(profile_breadcrumb)

    def _getBody(self, params):
        return self._getPageContent(params)


class WPUsersAdmin(WPAdmin):
    template_prefix = 'users/'

    def getJSFiles(self):
        return WPAdmin.getJSFiles(self) + self._asset_env['modules_users_js'].urls()
