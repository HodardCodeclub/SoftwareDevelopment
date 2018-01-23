

from flask import session
from werkzeug.exceptions import Forbidden

from fossir.modules.rb.controllers import RHRoomBookingBase
from fossir.modules.rb.util import rb_is_admin
from fossir.util.i18n import _


class RHRoomBookingAdminBase(RHRoomBookingBase):
    """
    Adds admin authorization. All classes that implement admin
    tasks should be derived from this class.
    """

    def _check_access(self):
        if session.user is None:
            self._require_user()
        elif not rb_is_admin(session.user):
            raise Forbidden(_('You are not authorized to take this action.'))
