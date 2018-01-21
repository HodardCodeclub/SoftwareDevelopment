

(function(global) {
    'use strict';

    global.setupProtectionWidget = function setupProtectionWidget(options) {
        options = $.extend(true, {
            fieldId: null,
            fieldName: null,
            parentProtected: false,
            aclFieldId: null,
            aclMessageUrl: null,
            hasInheritedAcl: false
        }, options);

        var inputs = $('input[name=' + options.fieldName + '][id^=' + options.fieldId + ']');
        var $enableAclLink = $('.enable-acl-link');
        var $aclListField = $('.acl-list-field');

        inputs.on('change', function() {
            var $this = $(this);
            var isProtected = $this.val() === 'protected' || ($this.val() === 'inheriting' && options.parentProtected);

            if (this.checked) {
                $('#form-group-protected-{0} .protection-message'.format(options.fieldId)).hide();
                $('#form-group-protected-{0} .{1}-protection-message'.format(options.fieldId, $this.val())).show();

                if (options.aclMessageUrl && options.hasInheritedAcl) {
                    $.ajax({
                        url: options.aclMessageUrl,
                        data: {mode: $this.val()},
                        error: handleAjaxError,
                        success: function(data) {
                            $this.closest('form').find('.inheriting-acl-message').html(data.html);
                        }
                    });
                }
                $aclListField.toggleClass('hidden', !isProtected);
                $enableAclLink.toggleClass('hidden', isProtected);
            }
        });

        $enableAclLink.on('click', function(evt) {
            evt.preventDefault();
            $('input[name=' + options.fieldName + '][value="protected"]').trigger('click');
        });

        _.defer(function() {
            inputs.trigger('change');
        });
    };
})(window);
