

from __future__ import unicode_literals

from fossir.modules.rb.controllers.user import event
from fossir.web.flask.wrappers import fossirBlueprint


event_mgmt = fossirBlueprint('event_mgmt', __name__, url_prefix='/event/<confId>/manage')


# Booking and event assignment list
event_mgmt.add_url_rule('/rooms/', 'rooms_booking_list', event.RHRoomBookingEventBookingList)
event_mgmt.add_url_rule('/rooms/choose-event', 'rooms_choose_event', event.RHRoomBookingEventChooseEvent)

# View/modify booking
event_mgmt.add_url_rule('/rooms/booking/<roomLocation>/<int:resvID>/', 'rooms_booking_details',
                        event.RHRoomBookingEventBookingDetails)
event_mgmt.add_url_rule('/rooms/booking/<roomLocation>/<int:resvID>/modify', 'rooms_booking_modify',
                        event.RHRoomBookingEventBookingModifyBooking, methods=('GET', 'POST'))
event_mgmt.add_url_rule('/rooms/booking/<roomLocation>/<int:resvID>/clone', 'rooms_booking_clone',
                        event.RHRoomBookingEventBookingCloneBooking, methods=('GET', 'POST'))
event_mgmt.add_url_rule('/rooms/booking/<roomLocation>/<int:resvID>/accept', 'rooms_booking_accept',
                        event.RHRoomBookingEventAcceptBooking, methods=('POST',))
event_mgmt.add_url_rule('/rooms/booking/<roomLocation>/<int:resvID>/cancel', 'rooms_booking_cancel',
                        event.RHRoomBookingEventCancelBooking, methods=('POST',))
event_mgmt.add_url_rule('/rooms/booking/<roomLocation>/<int:resvID>/reject', 'rooms_booking_reject',
                        event.RHRoomBookingEventRejectBooking, methods=('POST',))
event_mgmt.add_url_rule('/rooms/booking/<roomLocation>/<int:resvID>/<date>/cancel', 'rooms_booking_occurrence_cancel',
                        event.RHRoomBookingEventCancelBookingOccurrence, methods=('POST',))
event_mgmt.add_url_rule('/rooms/booking/<roomLocation>/<int:resvID>/<date>/reject', 'rooms_booking_occurrence_reject',
                        event.RHRoomBookingEventRejectBookingOccurrence, methods=('POST',))

# Book room
event_mgmt.add_url_rule('/rooms/room/<roomLocation>/<int:roomID>/book', 'rooms_room_book',
                        event.RHRoomBookingEventNewBookingSimple, methods=('GET', 'POST'))
event_mgmt.add_url_rule('/rooms/book', 'rooms_book', event.RHRoomBookingEventNewBooking, methods=('GET', 'POST'))

# Room details
event_mgmt.add_url_rule('/rooms/room/<roomLocation>/<int:roomID>/', 'rooms_room_details',
                        event.RHRoomBookingEventRoomDetails)
