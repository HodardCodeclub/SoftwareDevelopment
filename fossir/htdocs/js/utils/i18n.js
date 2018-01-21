

/* global Jed:false */

(function(global) {
    "use strict";

    var defaultI18n = new Jed({
        locale_data: global.TRANSLATIONS,
        domain: "fossir"
    });

    global.i18n = defaultI18n;
    global.$T = _.bind(defaultI18n.gettext, defaultI18n);

    ['gettext', 'ngettext', 'pgettext', 'npgettext', 'translate'].forEach(function(name) {
        global.$T[name] = _.bind(defaultI18n[name], defaultI18n);
    });

    global.$T.domain = _.memoize(function(domain) {
        return new Jed({
            locale_data: global.TRANSLATIONS,
            domain: domain
        });
    });
})(window);
