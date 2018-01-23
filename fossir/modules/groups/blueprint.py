

from __future__ import unicode_literals

from fossir.modules.groups.controllers import (RHGroupDelete, RHGroupDeleteMember, RHGroupDetails, RHGroupEdit,
                                               RHGroupMembers, RHGroups)
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('groups', __name__, template_folder='templates', virtual_template_folder='groups',
                      url_prefix='/admin/groups')


_bp.add_url_rule('/', 'groups', RHGroups, methods=('GET', 'POST'))
_bp.add_url_rule('/<provider>/<group_id>/', 'group_details', RHGroupDetails)
_bp.add_url_rule('/<provider>/<group_id>/members', 'group_members', RHGroupMembers)
_bp.add_url_rule('/fossir/new', 'group_add', RHGroupEdit, methods=('GET', 'POST'))
_bp.add_url_rule('/<any(fossir):provider>/<int:group_id>/edit', 'group_edit', RHGroupEdit, methods=('GET', 'POST'))
_bp.add_url_rule('/<any(fossir):provider>/<int:group_id>/delete', 'group_delete', RHGroupDelete, methods=('POST',))
_bp.add_url_rule('/<any(fossir):provider>/<int:group_id>/<int:user_id>', 'group_delete_member', RHGroupDeleteMember,
                 methods=('DELETE',))
