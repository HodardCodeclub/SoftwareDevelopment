

(function(global) {
    'use strict';

    global.setupEventCreationDialog = function setupEventCreationDialog(options) {
        options = $.extend({
            categoryField: null,
            protectionModeFields: null,
            initialCategory: null
        }, options);
        var messages = $($.parseHTML($('#event-creation-protection-messages').html()));
        var protectionMessage = $('<div>', {'class': 'form-group', 'css': {'marginTop': '5px'}});
        var currentCategory = null;

        protectionMessage.appendTo(options.protectionModeFields.closest('.form-field'));

        function updateProtectionMessage() {
            var mode = options.protectionModeFields.filter(':checked').val();
            if (mode == 'inheriting') {
                mode = currentCategory.is_protected ? 'inheriting-protected' : 'inheriting-public';
            }
            var elem = messages.filter('.{0}-protection-message'.format(mode));
            elem.find('.js-category-title').text(currentCategory.title);
            protectionMessage.html(elem);
        }

        options.categoryField.on('fossir:categorySelected', function(evt, category) {
            if (!currentCategory) {
                options.protectionModeFields.prop('disabled', false);
                options.protectionModeFields.filter('[value=inheriting]').prop('checked', true);
            }
            currentCategory = category;
            updateProtectionMessage();
        });

        options.protectionModeFields.on('change', function() {
            updateProtectionMessage();
        });

        if (options.initialCategory) {
            options.categoryField.trigger('fossir:categorySelected', [options.initialCategory]);
        } else {
            options.protectionModeFields.prop('disabled', true);
        }
    };
})(window);
