

from __future__ import unicode_literals

from fossir.core.celery.controllers import RHCeleryTasks
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('celery', __name__, url_prefix='/admin/tasks', template_folder='templates',
                      virtual_template_folder='celery')

_bp.add_url_rule('/', 'index', RHCeleryTasks)
