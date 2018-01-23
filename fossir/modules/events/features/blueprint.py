

from __future__ import unicode_literals

from fossir.modules.events.features.controllers import RHFeatures, RHSwitchFeature
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('event_features', __name__, template_folder='templates',
                      virtual_template_folder='events/features', url_prefix='/event/<confId>/manage/features')

_bp.add_url_rule('/', 'index', RHFeatures)
_bp.add_url_rule('/<feature>', 'switch', RHSwitchFeature, methods=('PUT', 'DELETE'))
