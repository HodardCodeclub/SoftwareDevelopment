
from __future__ import unicode_literals

from flask import session
from werkzeug.exceptions import Forbidden

from fossir.util.i18n import _
from fossir.web.rh import RHProtected


class RHAdminBase(RHProtected):
    """Base class for all admin-only RHs"""

    DENY_FRAMES = True

    def _check_access(self):
        RHProtected._check_access(self)
        if not session.user.is_admin:
            raise Forbidden(_("Only fossir administrators may access this page."))
