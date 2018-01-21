

(function($, global) {
    'use strict';

    $.fn.stickyTooltip = function(category, content) {
        return this.qtip({
            content: {
                text: content
            },
            position: {
                my: 'left middle',
                at: 'middle right'
            },
            hide: {
                'event': 'click unfocus'
            },
            style: {
                classes: 'qtip-' + category
            },
            show: {
                when: false,
                ready: true
            }
        });
    };

    global.repositionTooltips = function repositionTooltips() {
        $('.qtip').qtip('reposition');
    };
})(jQuery, window);
