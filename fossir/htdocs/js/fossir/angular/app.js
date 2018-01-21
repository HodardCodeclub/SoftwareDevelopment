

angular.module('nd', [
    'ndDirectives',
    'ndFilters',
    'ndServices',
    'nd.regform'
])

.controller('AppCtrl', function($scope) {
    // Main application controller.
    // This is a good place for logic not specific to the template or route
    // such as menu logic or page title wiring.
})
;
