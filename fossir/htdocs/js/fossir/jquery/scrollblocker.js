

(function($) {
    $.widget("fossir.scrollblocker", {

        options: {
            overflowType: "scroll"
        },

        _create: function() {
            var element = this.element;
            var options = this.options;

            $("body").on("mousewheel wheel", function (e) {
                var blocker = $(e.target).parentsUntil(element.parent()).filter(function(){
                    return $(this).hasCSS("overflow-y", options.overflowType);
                });

                if (blocker.length > 0) {
                    var wheelup = (e.originalEvent.wheelDelta || -e.originalEvent.deltaY) / 120 > 0;

                    if (blocker.scrollTop() === 0 && wheelup) {
                        return false;
                    }

                    if ((blocker.scrollTop()+1 >= (blocker.prop("scrollHeight") - blocker.outerHeight())) && !wheelup) {
                        return false;
                    }
                }

                return true;
            });
        }
    });
})(jQuery);
