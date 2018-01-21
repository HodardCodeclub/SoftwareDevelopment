

function go_to_room(roomLocation, roomId, clone_booking) {
    var url;
    if (clone_booking) {
        url = build_url(fossir.Urls.RoomBookingCloneBooking, {
            roomLocation: roomLocation,
            room: roomId,
            resvID: clone_booking
        });
    }
    else {
        url = build_url(fossir.Urls.RoomBookingBookRoom, {
            roomLocation: roomLocation,
            roomID: roomId
        });
    }

    fossirRequest('roomBooking.room.bookingPermission',
        {room_id: roomId},
        function(result, error) {
            if(!error) {
                if (result.can_book) {
                    window.location.href = url;
                } else {
                    var popup = new AlertPopup('Booking Not Allowed', "You're not allowed to book this room");
                    popup.open();
                }
            } else {
                showErrorDialog(error);
            }
        }
    );
}
