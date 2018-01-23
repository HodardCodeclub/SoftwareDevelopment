

from __future__ import unicode_literals

from fossir.modules.events.static.controllers import RHStaticSiteBuild, RHStaticSiteDownload, RHStaticSiteList
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('static_site', __name__, template_folder='templates', virtual_template_folder='events/static',
                      url_prefix='/event/<confId>/manage/offline-copy')

# Event management
_bp.add_url_rule('/', 'list', RHStaticSiteList)
_bp.add_url_rule('/<int:id>.zip', 'download', RHStaticSiteDownload)
_bp.add_url_rule('/build', 'build', RHStaticSiteBuild, methods=('POST',))
