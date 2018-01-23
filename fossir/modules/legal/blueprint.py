

from __future__ import unicode_literals

from fossir.modules.legal.controllers import RHDisplayLegalMessages, RHManageLegalMessages
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('legal', __name__, template_folder='templates', virtual_template_folder='legal')

_bp.add_url_rule('/admin/legal', 'manage', RHManageLegalMessages, methods=('GET', 'POST'))
_bp.add_url_rule('/tos', 'display_tos', RHDisplayLegalMessages)
