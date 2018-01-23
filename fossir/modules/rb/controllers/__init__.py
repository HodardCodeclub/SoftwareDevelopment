

from __future__ import unicode_literals

from flask import session
from werkzeug.exceptions import Forbidden, NotFound

from indico.core.config import config
from indico.modules.rb.util import rb_check_user_access
from indico.util.i18n import _
from indico.web.rh import RHProtected


class RHRoomBookingProtected(RHProtected):
    def _require_user(self):
        if not config.ENABLE_ROOMBOOKING:
            raise NotFound(_('The room booking module is not enabled.'))
        RHProtected._require_user(self)
        if not rb_check_user_access(session.user):
            raise Forbidden(_('Your are not authorized to access the room booking system.'))


class RHRoomBookingBase(RHRoomBookingProtected):
    """Base class for room booking RHs"""

    # legacy code might still show unsanitized content from the DB
    # so we need to keep the sanitizer running until everything in
    # roombooking has been moved to Jinja templates
    CHECK_HTML = True
