

from __future__ import unicode_literals

from fossir.modules.cephalopod.controllers import RHCephalopod, RHCephalopodSync, RHSystemInfo
from fossir.web.flask.wrappers import fossirBlueprint


cephalopod_blueprint = _bp = fossirBlueprint('cephalopod', __name__, template_folder='templates',
                                             virtual_template_folder='cephalopod')

_bp.add_url_rule('/admin/community-hub/', 'index', RHCephalopod, methods=('GET', 'POST'))
_bp.add_url_rule('/admin/community-hub/sync', 'sync', RHCephalopodSync, methods=('POST',))
_bp.add_url_rule('/system-info', 'system-info', RHSystemInfo)
