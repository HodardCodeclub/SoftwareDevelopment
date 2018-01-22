

from __future__ import unicode_literals

from fossir.modules.bootstrap.controllers import RHBootstrap
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('bootstrap', __name__, template_folder='templates', virtual_template_folder='bootstrap')
_bp.add_url_rule('/bootstrap', 'index', RHBootstrap, methods=('GET', 'POST'))
