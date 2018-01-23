

from flask import redirect

from fossir.modules.rb.controllers import RHRoomBookingBase
from fossir.modules.rb.models.locations import Location
from fossir.web.flask.util import url_for


class RHRoomBookingWelcome(RHRoomBookingBase):
    def _process(self):
        default_location = Location.default_location
        if default_location and default_location.is_map_available:
            return redirect(url_for('rooms.roomBooking-mapOfRooms'))
        else:
            return redirect(url_for('rooms.book'))
