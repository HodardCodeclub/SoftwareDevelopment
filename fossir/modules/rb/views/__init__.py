
from __future__ import unicode_literals

from flask import render_template_string

from fossir.util.i18n import _
from fossir.util.string import to_unicode
from fossir.web.breadcrumbs import render_breadcrumbs
from fossir.web.views import WPDecorated, WPJinjaMixin


class WPRoomBookingBase(WPJinjaMixin, WPDecorated):
    template_prefix = 'rb/'
    title = _('Room Booking')

    def __init__(self, rh, **kwargs):
        kwargs['active_menu_item'] = self.sidemenu_option
        WPDecorated.__init__(self, rh, **kwargs)

    def getJSFiles(self):
        return WPDecorated.getJSFiles(self) + self._includeJSPackage(['Management', 'RoomBooking'])

    def _get_breadcrumbs(self):
        return render_breadcrumbs(_('Room Booking'))

    def _getBody(self, params):
        return self._getPageContent(params)


class WPRoomBookingLegacyBase(WPRoomBookingBase):
    def _getBody(self, params):
        # Legacy handling for pages that do not use Jinja inheritance.
        tpl = "{% extends 'rb/base.html' %}{% block content %}{{ _body | safe }}{% endblock %}"
        body = to_unicode(self._getPageContent(params))
        return render_template_string(tpl, _body=body, **self._kwargs)

    def _getPageContent(self, params):
        raise NotImplementedError
