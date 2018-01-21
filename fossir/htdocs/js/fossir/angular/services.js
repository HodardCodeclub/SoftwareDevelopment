

var ndServices = angular.module('ndServices', []);

ndServices.provider('url', function() {
    var baseUrl = fossir.Urls.Base;
    var modulePath = '';
    // XXX: don't remove the () around `+Date.now()`
    // the minifier converts this to `'?'++Date.now()` which is a syntax error
    var debug = $('body').data('debug') ? '?' + (+Date.now()) : '';

    return {
        setModulePath: function(path) {
            if (path.substr(-1) == '/') {
                path = path.substr(0, path.length - 1);
            }

            modulePath = path;
        },

        $get: function() {
            return {
                tpl: function(path) {
                    return baseUrl + modulePath + '/tpls/' + path + debug;
                }
            };
        }
    };
});
