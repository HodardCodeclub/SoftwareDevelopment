

from __future__ import absolute_import

from fossir.legacy.common.TemplateExec import render


class MathjaxMixin(object):
    def _getHeadContent(self):
        return (render('js/mathjax.config.js.tpl') +
                b'\n'.join(b'<script src="{0}" type="text/javascript"></script>'.format(url)
                           for url in self._asset_env['mathjax_js'].urls()))
