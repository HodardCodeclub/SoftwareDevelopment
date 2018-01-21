

var ndFilters = angular.module("ndFilters", []);

ndFilters.filter("i18n", function() {
    return function(input) {
        var str = $T.gettext(input);
        if (arguments.length > 1) {
            str = str.format.apply(str, [].slice.call(arguments, 1));
        }
        return str;
    };
});

ndFilters.filter("range", function() {
    return function(input, min, max) {
        min = parseInt(min, 10) || 0;
        max = parseInt(max, 10);
        for (var i=min; i<=max; i++) {
            input.push(i);
        }
        return input;
    };
});
