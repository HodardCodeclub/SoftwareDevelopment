

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
