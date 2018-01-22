

from __future__ import unicode_literals

from fossir.modules.announcement.controllers import RHAnnouncement
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('announcement', __name__, template_folder='templates', virtual_template_folder='announcement')

_bp.add_url_rule('/admin/announcement', 'manage', RHAnnouncement, methods=('GET', 'POST'))
