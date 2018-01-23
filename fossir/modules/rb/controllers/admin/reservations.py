

from flask import flash, redirect, request, url_for

from fossir.core.db import db
from fossir.modules.rb.controllers.admin import RHRoomBookingAdminBase
from fossir.modules.rb.models.reservations import Reservation
from fossir.util.i18n import _


class RHRoomBookingDeleteBooking(RHRoomBookingAdminBase):
    def _process_args(self):
        self._reservation = Reservation.get_one(request.view_args['resvID'])

    def _process(self):
        db.session.delete(self._reservation)
        flash(_(u'Booking deleted'), 'success')
        return redirect(url_for('rooms.roomBooking-search4Bookings'))
