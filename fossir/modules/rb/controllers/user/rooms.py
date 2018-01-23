
import re
from datetime import date, datetime, time, timedelta

from dateutil.relativedelta import relativedelta
from flask import request, session
from sqlalchemy import func
from werkzeug.datastructures import MultiDict

from fossir.core.db import db
from fossir.core.errors import fossirError
from fossir.modules.rb.controllers import RHRoomBookingBase
from fossir.modules.rb.controllers.decorators import requires_location, requires_room
from fossir.modules.rb.forms.rooms import SearchRoomsForm
from fossir.modules.rb.models.equipment import EquipmentType
from fossir.modules.rb.models.locations import Location
from fossir.modules.rb.models.reservation_occurrences import ReservationOccurrence
from fossir.modules.rb.models.reservations import Reservation
from fossir.modules.rb.models.rooms import Room
from fossir.modules.rb.statistics import calculate_rooms_occupancy, compose_rooms_stats
from fossir.modules.rb.views.user.rooms import (WPRoomBookingMapOfRooms, WPRoomBookingMapOfRoomsWidget,
                                                WPRoomBookingRoomDetails, WPRoomBookingRoomStats,
                                                WPRoomBookingSearchRooms, WPRoomBookingSearchRoomsResults)
from fossir.web.forms.base import FormDefaults


class RHRoomBookingMapOfRooms(RHRoomBookingBase):
    def _process_args(self):
        RHRoomBookingBase._process_args(self)
        self._room_id = request.args.get('roomID')

    def _process(self):
        return WPRoomBookingMapOfRooms.render_template('map.html', room_id=self._room_id)


class RHRoomBookingMapOfRoomsWidget(RHRoomBookingBase):
    def _process_args(self):
        RHRoomBookingBase._process_args(self)
        self._room_id = request.args.get('roomID')

    def _process(self):
        return WPRoomBookingMapOfRoomsWidget(self, roomID=self._room_id).display()


class RHRoomBookingSearchRooms(RHRoomBookingBase):
    menu_item = 'search_rooms'
    CSRF_ENABLED = False

    def _get_form_data(self):
        return request.form

    def _process_args(self):
        defaults = FormDefaults(location=Location.default_location)
        self._form = SearchRoomsForm(self._get_form_data(), obj=defaults, csrf_enabled=False)
        if (not session.user or not Room.user_owns_rooms(session.user)) and not hasattr(self, 'search_criteria'):
            # Remove the form element if the user has no rooms and we are not using a shortcut
            del self._form.is_only_my_rooms

    def _is_submitted(self):
        return self._form.is_submitted()

    def _process(self):
        form = self._form
        if self._is_submitted() and form.validate():
            rooms = Room.find_with_filters(form.data, session.user)
            return WPRoomBookingSearchRoomsResults(self, self.menu_item, rooms=rooms).display()
        equipment_locations = {eq.id: eq.location_id for eq in EquipmentType.find()}
        return WPRoomBookingSearchRooms(self, form=form, errors=form.error_list, rooms=Room.find_all(is_active=True),
                                        equipment_locations=equipment_locations).display()


class RHRoomBookingSearchRoomsShortcutBase(RHRoomBookingSearchRooms):
    """Base class for searches with predefined criteria"""
    search_criteria = {}

    def _is_submitted(self):
        return True

    def _get_form_data(self):
        return MultiDict(self.search_criteria)


class RHRoomBookingSearchMyRooms(RHRoomBookingSearchRoomsShortcutBase):
    menu_item = 'room_list'
    search_criteria = {
        'is_only_my_rooms': True,
        'location': None
    }


class RHRoomBookingRoomDetails(RHRoomBookingBase):
    @requires_location
    @requires_room
    def _process_args(self):
        self._calendar_start = datetime.combine(date.today(), time())
        self._calendar_end = datetime.combine(date.today(), time(23, 59))
        try:
            preview_months = int(request.args.get('preview_months', '0'))
        except (TypeError, ValueError):
            preview_months = 0
        self._calendar_end += timedelta(days=31 * preview_months)

    def _get_view(self, **kwargs):
        return WPRoomBookingRoomDetails(self, **kwargs)

    def _process(self):
        occurrences = ReservationOccurrence.find(
            Reservation.room_id == self._room.id,
            ReservationOccurrence.start_dt >= self._calendar_start,
            ReservationOccurrence.end_dt <= self._calendar_end,
            ReservationOccurrence.is_valid,
            _join=ReservationOccurrence.reservation,
            _eager=ReservationOccurrence.reservation
        ).options(ReservationOccurrence.NO_RESERVATION_USER_STRATEGY).all()

        return self._get_view(room=self._room, start_dt=self._calendar_start, end_dt=self._calendar_end,
                              occurrences=occurrences).display()


class RHRoomBookingRoomStats(RHRoomBookingBase):
    def _process_args(self):
        self._room = Room.get(request.view_args['roomID'])
        self._occupancy_period = request.args.get('period', 'pastmonth')
        self._end = date.today()
        if self._occupancy_period == 'pastmonth':
            self._end = self._end - relativedelta(days=1)
            self._start = self._end - relativedelta(days=29)
        elif self._occupancy_period == 'thisyear':
            self._start = date(self._end.year, 1, 1)
        elif self._occupancy_period == 'sinceever':
            oldest = db.session.query(func.min(Reservation.start_dt)).filter_by(room_id=self._room.id).scalar()
            self._start = oldest.date() if oldest else self._end
        else:
            match = re.match(r'(\d{4})(?:-(\d{2}))?', self._occupancy_period)
            if match is None:
                raise fossirError(u'Invalid period specified')
            year = int(match.group(1))
            month = int(match.group(2)) if match.group(2) else None
            if month:
                try:
                    self._start = date(year, month, 1)
                except ValueError:
                    raise fossirError(u'Invalid year or month specified')
                self._end = self._start + relativedelta(months=1)
                self._occupancy_period = '{:d}-{:02d}'.format(year, month)
            else:
                try:
                    self._start = date(year, 1, 1)
                except ValueError:
                    raise fossirError(u'Invalid year specified')
                self._end = self._start + relativedelta(years=1)
                self._occupancy_period = str(year)

    def _process(self):
        last_year = str(date.today().year - 1)
        last_month_date = date.today() - relativedelta(months=1, day=1)
        last_month = '{:d}-{:02d}'.format(last_month_date.year, last_month_date.month)
        return WPRoomBookingRoomStats(self,
                                      room=self._room,
                                      period=self._occupancy_period,
                                      last_year=last_year,
                                      last_month=last_month,
                                      occupancy=calculate_rooms_occupancy([self._room], self._start, self._end),
                                      stats=compose_rooms_stats([self._room])).display()
