

from __future__ import unicode_literals

from fossir.util.i18n import _
from fossir.web.breadcrumbs import render_breadcrumbs
from fossir.web.menu import get_menu_item
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPAdmin(WPJinjaMixin, WPDecorated):
    """Base class for admin pages."""

    def __init__(self, rh, active_menu_item=None, **kwargs):
        kwargs['active_menu_item'] = active_menu_item or self.sidemenu_option
        WPDecorated.__init__(self, rh, **kwargs)

    def _get_breadcrumbs(self):
        menu_item = get_menu_item('admin-sidemenu', self._kwargs['active_menu_item'])
        items = [_('Administration')]
        if menu_item:
            items.append(menu_item.title)
        return render_breadcrumbs(*items)

    def _getBody(self, params):
        return self._getPageContent(params)
