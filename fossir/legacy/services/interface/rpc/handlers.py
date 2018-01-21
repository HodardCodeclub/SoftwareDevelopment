

from importlib import import_module

from fossir.modules.rb import services as rb_services
from fossir.modules.rb.services import aspects as rb_aspect_services
from fossir.modules.rb.services import blockings as rb_blocking_services
from fossir.modules.rb.services import rooms as rb_room_services


methodMap = {
    # rb base
    'roomBooking.getDateWarning': rb_services.GetDateWarning,
    # rb rooms
    'roomBooking.rooms.availabilitySearch': rb_room_services.RoomBookingAvailabilitySearchRooms,
    'roomBooking.locationsAndRooms.listWithGuids': rb_room_services.RoomBookingListLocationsAndRoomsWithGuids,
    'roomBooking.room.bookingPermission': rb_room_services.BookingPermission,
    # rb aspects
    'roomBooking.mapaspects.create': rb_aspect_services.RoomBookingMapCreateAspect,
    'roomBooking.mapaspects.update': rb_aspect_services.RoomBookingMapUpdateAspect,
    'roomBooking.mapaspects.remove': rb_aspect_services.RoomBookingMapRemoveAspect,
    'roomBooking.mapaspects.list': rb_aspect_services.RoomBookingMapListAspects,
    # rb blockings
    'roombooking.blocking.approve': rb_blocking_services.RoomBookingBlockingApprove,
    'roombooking.blocking.reject': rb_blocking_services.RoomBookingBlockingReject,
}


endpointMap = {
    "search": import_module('fossir.legacy.services.implementation.search')
}
