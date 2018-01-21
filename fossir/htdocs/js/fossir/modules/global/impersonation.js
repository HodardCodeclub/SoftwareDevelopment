

/* global ChooseUsersPopup:false */

(function() {
    'use strict';

    function sendRequest(url, payload) {
        $.ajax({
            url: url,
            method: 'POST',
            data: payload,
            complete: IndicoUI.Dialogs.Util.progress(),
            error: handleAjaxError,
            success: function() {
                IndicoUI.Dialogs.Util.progress();
                location.reload();
            }
        });
    }

    function impersonateUser(url) {
        function _userSelected(users) {
            sendRequest(url, {user_id: users[0].id});
        }

        var dialog = new ChooseUsersPopup(
            $T("Select user to impersonate"),
            true, null, false, true, null, true, true, false, _userSelected, null, false
        );

        dialog.execute();
    }

    function undoImpersonateUser(url) {
        sendRequest(url, {undo: '1'});
    }

    $(document).ready(function() {
        $('.login-as').on('click', function(evt) {
            evt.preventDefault();
            impersonateUser($(this).data('href'));
        });

        $('.undo-login-as').on('click', function(evt) {
            evt.preventDefault();
            undoImpersonateUser($(this).data('href'));
        });
    });
})();
