

from fossir.legacy.webinterface.wcomponents import WTemplated
from fossir.modules.rb.views.admin import WPRoomBookingAdminBase
from fossir.util.i18n import _


class WPRoomBookingAdmin(WPRoomBookingAdminBase):
    subtitle = _(u'Locations')

    def _get_legacy_content(self, params):
        return WTemplated('RoomBookingAdmin').getHTML(params)


class WPRoomBookingAdminLocation(WPRoomBookingAdminBase):
    sidemenu_option = 'rb-rooms'

    @property
    def subtitle(self):
        return self._kwargs['location'].name

    def _get_legacy_content(self, params):
        return WTemplated('RoomBookingAdminLocation').getHTML(params)
