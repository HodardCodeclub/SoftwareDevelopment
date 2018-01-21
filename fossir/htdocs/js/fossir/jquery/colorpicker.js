
(function($) {
    'use strict';

    $.widget("fossir.colorpicker", {

        options: {
            defaultColor: "ffffff"
        },

        _create: function() {
            var self = this;
            var element = self.element;
            var opt = self.options;
            var clickableWrapper = element.find('.clickable-wrapper');
            var preview = element.find('.color-preview');
            var colorInput = element.find('input');

            function updateColorPreview(color) {
                preview.css('background', color).removeClass('no-value');
            }

            function updateWidget() {
                preview.toggleClass('no-value', !colorInput.val().length);
                if (colorInput.val()) {
                    updateColorPreview(colorInput.val());
                    clickableWrapper.ColorPickerSetColor(colorInput.val());
                }
                else {
                    preview.attr('style', null);
                }
            }

            colorInput.on('input change', updateWidget);

            clickableWrapper.ColorPicker({
                color: opt.defaultColor,
                onSubmit: function(hsb, hex, rgb, el) {
                    $(el).val(hex);
                    updateColorPreview('#' + hex);
                    $(el).ColorPickerHide();
                },
                onChange: function(hsb, hex) {
                    colorInput.val('#' + hex);
                    updateColorPreview('#' + hex);
                    colorInput.trigger('input');
                },
                onShow: function(colorpicker) {
                    $(colorpicker).fadeIn(500);
                    return false;
                },
                onHide: function(colorpicker) {
                    $(colorpicker).fadeOut(500);
                    return false;
                }
            });

            updateWidget();
        }
    });
})(jQuery);
