

(function(global) {
    'use strict';

    global.setupCategoryPickerWidget = function setupCategoryPickerWidget(options) {
        options = $.extend(true, {
            fieldId: null,
            navigatorCategoryId: null,
            requireEventCreationRights: false,
            allow: {
                events: true,
                subcats: true
            }
        }, options);

        var $field = $('#' + options.fieldId);
        var $categoryTitle = $('#category-title-' + options.fieldId);
        var $dialogTrigger = $('#categorynav-button-' + options.fieldId);
        var hiddenData = $field.val() ? JSON.parse($field.val()) : {};
        var navigatorCategory = options.navigatorCategoryId;
        var actionOn = {};

        if (options.requireEventCreationRights) {
            actionOn.categoriesWithoutEventCreationRights = {disabled: true};
        }
        if (!options.allow.events) {
            actionOn.categoriesWithEvents = {disabled: true};
        }
        if (!options.allow.subcats) {
            actionOn.categoriesWithSubcategories = {disabled: true};
        }

        if (hiddenData) {
            $categoryTitle.text(hiddenData.title);
            $field.val(JSON.stringify(hiddenData));
        }

        $.ajax({
            url: build_url(fossir.Urls.Categories.info, {category_id: navigatorCategory}),
            dataType: 'json',
            error: handleAjaxError,
            success: function(data) {
                navigatorCategory = data;
            }
        });

        $dialogTrigger.on('click', function(evt) {
            evt.preventDefault();
            $('<div>').categorynavigator({
                category: navigatorCategory,
                openInDialog: true,
                actionOn: actionOn,
                onAction: function(category) {
                    var event = $.Event('fossir:categorySelected');
                    var dfd = $.Deferred();
                    $categoryTitle.text(category.title);
                    hiddenData = {id: category.id, title: category.title};
                    navigatorCategory = category.id;
                    $field.val(JSON.stringify(hiddenData)).trigger('change').trigger(event, [category, dfd]);
                    if (event.isDefaultPrevented()) {
                        return dfd;
                    }
                }
            });
        });
    };
})(window);
