
// Comments the repeatition for user, to make it clear
function set_repeatition_comment() {
    var s = '';
    var repType = parseInt($('#repeatability').val(), 10);
    if(repType > 0) {
        var date = new Date(parseInt($('#sYear').val(), 10), parseInt($('#sMonth').val()-1, 10), parseInt($('#sDay').val(), 10));
        var weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        s = 'on ' + weekDays[date.getDay()];
        if(repType == 4) {
            var weekNr = Math.floor( date.getDate() / 7 ) + 1;
            var postfix = ['st', 'nd', 'rd', 'th', 'th'];
            var weekNrStr = 'the ' + weekNr + postfix[weekNr-1] + ' ';
            s = 'on ' + weekNrStr + weekDays[date.getDay()] + ' of a month';
        }
    }
    $('#repComment').html(s);
}

// Store all fields in local storage
function saveFormData() {
    var selectedRooms = $("#roomselector").roomselector("selection");
    var filterData = $("#roomselector").roomselector("userdata");

    var rbDict = {
        startDate: $('#sDatePlace').datepicker('getDate'),
        endDate: $('#eDatePlace').datepicker('getDate'),
        startTime: $('#timerange').timerange('getStartTime'),
        endTime: $('#timerange').timerange('getEndTime'),
        "capacity": filterData.capacity,
        "videoconference": filterData.videoconference,
        "webcast": filterData.webcast,
        "projector": filterData.projector,
        "publicroom": filterData.publicroom,
        "filter": filterData.search,
        "selectedRooms": selectedRooms,
        "finishDate": $('#finishDate').val(),
        "flexibleDatesRange": $("#flexibleDates input[name=flexible_dates_range]:checked").val(),
        repeatFrequency: $('input[name=repeat_frequency]:checked').val(),
        repeatInterval: $('#repeat_interval').val(),
        roomIds: $('#room_ids').val()
    };

    $.jStorage.set(userId, rbDict);
    $.jStorage.setTTL(userId, 7200000); // 2 hours
}

$(document).ready(function() {
    var backLink = $('#js-back-to-period');
    if (backLink.length) {
        var data = $.jStorage.get(userId);
        if (!data || !data.startDate) {
            backLink.contents().unwrap();
        }
        else {
            backLink.on('click', function(e) {
                e.preventDefault();
                var form = $('<form>', {
                    method: 'POST',
                    action: ''
                });
                form.append([
                    $('<input>', {type: 'hidden', name: 'step', value: 1}),
                    $('<input>', {type: 'hidden', name: 'start_dt', value: moment(data.startDate).format('D/MM/YYYY') + ' ' + data.startTime}),
                    $('<input>', {type: 'hidden', name: 'end_dt', value: moment(data.endDate).format('D/MM/YYYY') + ' ' + data.endTime}),
                    $('<input>', {type: 'hidden', name: 'repeat_frequency', value: data.repeatFrequency}),
                    $('<input>', {type: 'hidden', name: 'repeat_interval', value: data.repeatInterval}),
                    $('<input>', {type: 'hidden', name: 'flexible_dates_range', value: data.flexibleDatesRange})
                ]);
                form.append($.map(data.roomIds, function(value) {
                    return $('<input>', {type: 'hidden', name: 'room_ids', value: value});
                }));
                form.appendTo(document.body).submit();
            });
        }
    }
});
