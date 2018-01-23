

from fossir.legacy.webinterface.wcomponents import WTemplated
from fossir.modules.rb.views import WPRoomBookingLegacyBase


class WPRoomBookingBlockingDetails(WPRoomBookingLegacyBase):
    sidemenu_option = 'blocking_create'

    def _getPageContent(self, params):
        return WTemplated('RoomBookingBlockingDetails').getHTML(params)


class WPRoomBookingBlockingForm(WPRoomBookingLegacyBase):
    sidemenu_option = 'blocking_create'

    def _getPageContent(self, params):
        return WTemplated('RoomBookingBlockingForm').getHTML(params)


class WPRoomBookingBlockingList(WPRoomBookingLegacyBase):
    sidemenu_option = 'my_blockings'

    def _getPageContent(self, params):
        return WTemplated('RoomBookingBlockingList').getHTML(params)


class WPRoomBookingBlockingsForMyRooms(WPRoomBookingLegacyBase):
    sidemenu_option = 'blockings_my_rooms'

    def _getPageContent(self, params):
        return WTemplated('RoomBookingBlockingsForMyRooms').getHTML(params)
