

from __future__ import unicode_literals

from flask import session
from werkzeug.exceptions import Forbidden

from fossir.core.errors import UserValueError
from fossir.legacy.services.implementation.base import ServiceBase
from fossir.modules.rb.models.blocked_rooms import BlockedRoom
from fossir.modules.rb.util import rb_is_admin
from fossir.util.i18n import _


class RoomBookingBlockingProcessBase(ServiceBase):
    UNICODE_PARAMS = True

    def _process_args(self):
        self.blocked_room = BlockedRoom.get(self._params['blocked_room_id'])

    def _check_access(self):
        user = session.user
        if not user or (not rb_is_admin(user) and not self.blocked_room.room.is_owned_by(user)):
            raise Forbidden(_('You are not permitted to modify this blocking'))


class RoomBookingBlockingApprove(RoomBookingBlockingProcessBase):
    def _getAnswer(self):
        self.blocked_room.approve()
        return {'state': self.blocked_room.state_name}


class RoomBookingBlockingReject(RoomBookingBlockingProcessBase):
    def _process_args(self):
        RoomBookingBlockingProcessBase._process_args(self)
        self.reason = self._params.get('reason')
        if not self.reason:
            raise UserValueError(_('You have to specify a rejection reason'))

    def _getAnswer(self):
        self.blocked_room.reject(session.user, self.reason)
        return {'state': self.blocked_room.state_name}
