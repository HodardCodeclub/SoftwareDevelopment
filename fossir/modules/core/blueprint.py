

from __future__ import unicode_literals

from fossir.modules.core.controllers import (RHChangeLanguage, RHChangeTimezone, RHContact, RHReportError, RHSettings,
                                             RHVersionCheck)
from fossir.web.flask.util import redirect_view
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('core', __name__, template_folder='templates', virtual_template_folder='core')

_bp.add_url_rule('/admin/settings/', 'settings', RHSettings, methods=('GET', 'POST'))
_bp.add_url_rule('/admin/version-check', 'version_check', RHVersionCheck)

# TODO: replace with an actual admin dashboard at some point
_bp.add_url_rule('/admin/', 'admin_dashboard', view_func=redirect_view('.settings'))

# Global operations
_bp.add_url_rule('/change-language', 'change_lang', RHChangeLanguage, methods=('POST',))
_bp.add_url_rule('/change-timezone', 'change_tz', RHChangeTimezone, methods=('POST',))

# Misc pages
_bp.add_url_rule('/contact', 'contact', RHContact)
_bp.add_url_rule('/report-error/<error_id>', 'report_error', RHReportError, methods=('GET', 'POST'))

# Allow loadbalancers etc to easily check whether the service is alive
_bp.add_url_rule('/ping', 'ping', lambda: ('', 204))
