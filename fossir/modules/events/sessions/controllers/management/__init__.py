

from __future__ import unicode_literals

from flask import request, session
from werkzeug.exceptions import Forbidden

from fossir.modules.events.management.controllers import RHManageEventBase
from fossir.modules.events.sessions.models.sessions import Session


class RHManageSessionsBase(RHManageEventBase):
    """Base RH for all session management RHs"""


class RHManageSessionBase(RHManageSessionsBase):
    """Base RH for management of a single session"""

    normalize_url_spec = {
        'locators': {
            lambda self: self.session
        }
    }

    def _process_args(self):
        RHManageSessionsBase._process_args(self)
        self.session = Session.get_one(request.view_args['session_id'], is_deleted=False)

    def _check_access(self):
        if not self.session.can_manage(session.user):
            raise Forbidden


class RHManageSessionsActionsBase(RHManageSessionsBase):
    """Base class for classes performing actions on sessions"""

    def _process_args(self):
        RHManageSessionsBase._process_args(self)
        session_ids = set(map(int, request.form.getlist('session_id')))
        self.sessions = Session.query.with_parent(self.event).filter(Session.id.in_(session_ids)).all()
