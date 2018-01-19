/* This file is part of fossir.
 * Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
 *
 * fossir is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 3 of the
 * License, or (at your option) any later version.
 *
 * fossir is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with fossir; if not, see <http://www.gnu.org/licenses/>.
 */

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
