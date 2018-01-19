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

(function(global) {
    'use strict';

    global.processJqPlotOptions = function processJqPlotOptions(options) {
        var jqPlotDefaultOptions = {
            animate: !$.jqplot.use_excanvas,
            animateReplot: !$.jqplot.use_excanvas,
            axesDefaults: {
                labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                tickOptions: {
                    markSize: 0,
                    formatString: '%d'
                }
            },
            cursor: {
                show: true,
                showTooltip: false,
                zoom: false
            },
            grid: {
                background: 'transparent',
                drawBorder: false,
                shadow: false
            },
            highlighter: {show: true},
            legend: {show: false},
            seriesColors: ['#007CAC'], // fossir blue
            seriesDefaults: {
                markerOptions: {
                    style: 'filledCircle',
                    color: '#007CAC' // fossir blue
                },
                lineWidth: 3,
                pointLabels: {
                    show: false,
                    color: 'white',
                    location: 'w',
                    xpadding: 4,
                    edgeTolerance: -2
                },
                rendererOptions: {
                    animation: {speed: 1000},
                    highlightColors: '#0085B9',
                    smooth: true
                },
                shadow: false,
                size: 11
            }
        };
        return $.extend(true, {}, jqPlotDefaultOptions, options);
    };

    $(document).ready(function() {
        $('.i-progress > .i-progress-bar').width(function getProgress() {
            return $(this).data('progress');
        });
        // Animate numerical values in badges
        $('.i-badge .i-badge-value[data-value]').each(function loadValue() {
            var $this = $(this);
            var val = $this.data('value');
            if (!_.isNumber(val) || val === 0) {
                $this.text(val);
                return;
            }
            $({Counter: 0}).animate({Counter: val}, {
                duration: 1000,
                easing: 'swing',
                step: function() {
                    $this.text(Math.ceil(this.Counter));
                }
            });
        });
    });
})(window);
