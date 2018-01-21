

(function($) {
    'use strict';

    $.widget("fossir.nullableselector", {

        options: {
            nullvalue: "__None"
        },

        _create: function() {
            var self = this;
            var element = self.element;
            var opt = self.options;

            element.toggleClass('no-value', element.val() === opt.nullvalue);
            element.on('change', function() {
                $(this).toggleClass('no-value', $(this).val() === opt.nullvalue);
            });
        }
    });
})(jQuery);
