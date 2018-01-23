

from __future__ import unicode_literals

from fossir.modules.events.logs.controllers import RHEventLogs
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('event_logs', __name__, template_folder='templates', virtual_template_folder='events/logs',
                      url_prefix='/event/<confId>/manage/logs')

_bp.add_url_rule('/', 'index', RHEventLogs)
