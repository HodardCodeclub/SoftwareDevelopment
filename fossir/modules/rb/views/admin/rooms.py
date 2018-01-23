

from fossir.legacy.webinterface.wcomponents import WTemplated
from fossir.modules.rb.views.admin import WPRoomBookingAdminBase
from fossir.util.i18n import _


class WPRoomBookingRoomForm(WPRoomBookingAdminBase):
    sidemenu_option = 'rb-rooms'

    @property
    def subtitle(self):
        room = self._kwargs['room']
        location = self._kwargs['location']
        if room.id is not None:
            return _(u'{location}: Edit room: {room}').format(room=room.full_name, location=location.name)
        else:
            return _(u'{location}: Create room').format(location=location.name)

    def _get_legacy_content(self, params):
        return WTemplated('RoomBookingRoomForm').getHTML(params)
