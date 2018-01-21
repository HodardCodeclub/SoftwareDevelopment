

(function(global) {
    'use strict';

    global.setupTypeaheadWidget = function setupTypeaheadWidget(options) {
        options = $.extend(true, {
            fieldId: null,
            minTriggerLength: 0,
            data: null,
            typeaheadOptions: null,
            searchUrl: null
        }, options);

        var field = $('#' + options.fieldId);
        var params = {
            hint: true,
            cancelButton: false,
            mustSelectItem: true,
            minLength: options.minTriggerLength,
            source: {
                data: options.data
            }
        };

        if (options.searchUrl) {
            $.extend(true, params, {
                dynamic: true,
                source: {
                    url: [{
                        url: options.searchUrl,
                        data: {
                            q: '{{query}}'
                        }
                    }]
                }
            });
        }

        field.typeahead($.extend(true, params, options.typeaheadOptions));
    };
})(window);
