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

/* global Palette:false */

(function(global) {
    'use strict';

    // base colors (must match entries in _palette.scss)
    global.Palette = {
        blue: '#5d95ea'
    };

    // colors for specific purposes
    Palette.highlight = Palette.blue;
})(window);