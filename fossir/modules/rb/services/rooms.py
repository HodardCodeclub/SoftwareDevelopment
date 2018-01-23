

from datetime import datetime

from flask import session

from fossir.core.config import config
from fossir.legacy.services.implementation.base import LoggedOnlyService, ServiceBase
from fossir.modules.rb.models.blockings import Blocking
from fossir.modules.rb.models.reservations import RepeatFrequency
from fossir.modules.rb.models.room_nonbookable_periods import NonBookablePeriod
from fossir.modules.rb.models.rooms import Room
from fossir.util.date_time import get_datetime_from_request


class RoomBookingAvailabilitySearchRooms(ServiceBase):
    UNICODE_PARAMS = True

    def _process_args(self):
        self._start_dt = get_datetime_from_request(prefix='start_', source=self._params)
        self._end_dt = get_datetime_from_request(prefix='end_', source=self._params)
        repetition = map(int, self._params['repeatability'].split('|'))
        self._repetition = RepeatFrequency(repetition[0]), repetition[1]

    def _getAnswer(self):
        rooms = Room.find_all(Room.filter_available(self._start_dt, self._end_dt, self._repetition))
        return [room.id for room in rooms]


class RoomBookingListLocationsAndRoomsWithGuids(ServiceBase):
    UNICODE_PARAMS = True

    def _process_args(self):
        self._isActive = self._params.get('isActive', None)

    def _getAnswer(self):
        if not config.ENABLE_ROOMBOOKING:
            return {}
        criteria = {'_eager': Room.location}
        if self._isActive is not None:
            criteria['is_active'] = self._isActive
        rooms = Room.find_all(**criteria)
        return {room.id: '{}: {}'.format(room.location_name, room.full_name) for room in rooms}


class BookingPermission(LoggedOnlyService):
    UNICODE_PARAMS = True

    def _process_args(self):
        blocking_id = self._params.get('blocking_id')
        self._room = Room.get(self._params['room_id'])
        self._blocking = Blocking.get(blocking_id) if blocking_id else None
        if 'start_dt' in self._params and 'end_dt' in self._params:
            start_dt = datetime.strptime(self._params['start_dt'], '%H:%M %Y-%m-%d')
            end_dt = datetime.strptime(self._params['end_dt'], '%H:%M %Y-%m-%d')
            self._nonbookable = bool(NonBookablePeriod.find_first(NonBookablePeriod.room_id == self._room.id,
                                                                  NonBookablePeriod.overlaps(start_dt, end_dt)))
        else:
            self._nonbookable = False

    def _getAnswer(self):
        user = session.user
        return {
            'blocked': not self._blocking.can_be_overridden(user, self._room) if self._blocking else self._nonbookable,
            'blocking_type': 'blocking' if self._blocking else 'nonbookable' if self._nonbookable else None,
            'is_reservable': self._room.is_reservable,
            'can_book': self._room.can_be_booked(user) or self._room.can_be_prebooked(user),
            'group': self._room.get_attribute_value('allowed-booking-group')
        }
