

(function(global) {
    'use strict';

    global.setupLinkingWidget = function setupLinkingWidget(options) {
        options = $.extend(true, {
            fieldId: null
        }, options);

        function updateDropdownState() {
            var $this = $(this);
            if ($this.prop('checked')) {
                $this.closest('.i-radio').siblings('.i-radio').find('.i-linking-dropdown select').prop('disabled', true);
                $this.siblings('.i-linking-dropdown').find('select').prop('disabled', false);
            }
        }

        var field = $('#' + options.fieldId);
        field.find('.i-linking > .i-linking-dropdown > select > option[value=""]').prop('disabled', true);
        field.find('.i-linking.i-radio > input[type="radio"]')
            .off('change').on('change', updateDropdownState)
            .each(updateDropdownState);
    };
})(window);
