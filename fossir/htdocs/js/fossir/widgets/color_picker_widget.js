
(function(global) {
    'use strict';

    global.setupColorPickerWidget = function setupColorPickerWidget(options) {
        options = $.extend(true, {
            fieldId: null
        }, options);

        var field = $('#' + options.fieldId);
        field.closest('.i-color-field').colorpicker();
        field.clearableinput();
    };
})(window);
