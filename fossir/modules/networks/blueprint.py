

from __future__ import unicode_literals

from fossir.modules.networks.controllers import (RHCreateNetworkGroup, RHDeleteNetworkGroup, RHEditNetworkGroup,
                                                 RHManageNetworks)
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('networks', __name__, template_folder='templates', virtual_template_folder='networks')

_bp.add_url_rule('/admin/networks/', 'manage', RHManageNetworks)
_bp.add_url_rule('/admin/networks/create', 'create_group', RHCreateNetworkGroup, methods=('GET', 'POST'))
_bp.add_url_rule('/admin/networks/<int:network_group_id>/', 'edit_group', RHEditNetworkGroup, methods=('GET', 'POST'))
_bp.add_url_rule('/admin/networks/<int:network_group_id>/delete', 'delete_group', RHDeleteNetworkGroup,
                 methods=('GET', 'POST'))
