

from __future__ import unicode_literals

from fossir.core.plugins.controllers import RHPluginDetails, RHPlugins
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('plugins', __name__, template_folder='templates', virtual_template_folder='plugins',
                      url_prefix='/admin/plugins')

_bp.add_url_rule('/', 'index', RHPlugins)
_bp.add_url_rule('/<plugin>/', 'details', RHPluginDetails, methods=('GET', 'POST'))
