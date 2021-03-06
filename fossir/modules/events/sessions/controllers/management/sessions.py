

from __future__ import unicode_literals

from flask import jsonify, request
from sqlalchemy.orm import subqueryload, undefer
from werkzeug.exceptions import BadRequest

from fossir.core.db import db
from fossir.core.db.sqlalchemy.colors import ColorTuple
from fossir.core.db.sqlalchemy.protection import ProtectionMode, render_acl
from fossir.modules.events.contributions.models.contributions import Contribution
from fossir.modules.events.management.controllers.base import RHContributionPersonListMixin
from fossir.modules.events.sessions.controllers.management import (RHManageSessionBase, RHManageSessionsActionsBase,
                                                                   RHManageSessionsBase)
from fossir.modules.events.sessions.forms import MeetingSessionBlockForm, SessionForm, SessionProtectionForm
from fossir.modules.events.sessions.models.blocks import SessionBlock
from fossir.modules.events.sessions.models.sessions import Session
from fossir.modules.events.sessions.operations import (create_session, delete_session, update_session,
                                                       update_session_block)
from fossir.modules.events.sessions.util import generate_pdf_from_sessions, generate_spreadsheet_from_sessions
from fossir.modules.events.sessions.views import WPManageSessions
from fossir.modules.events.util import get_random_color, update_object_principals
from fossir.util.spreadsheets import send_csv, send_xlsx
from fossir.web.flask.templating import get_template_module
from fossir.web.flask.util import send_file
from fossir.web.forms.base import FormDefaults
from fossir.web.forms.colors import get_colors
from fossir.web.forms.util import get_form_field_names
from fossir.web.util import jsonify_data, jsonify_form, jsonify_template


def _get_session_list_args(event):
    sessions = (Session.query.with_parent(event)
                .options(undefer('attachment_count'),
                         subqueryload('blocks').undefer('contribution_count'))
                .order_by(db.func.lower(Session.title))
                .all())
    return {'sessions': sessions, 'default_colors': get_colors()}


def _render_session_list(event):
    tpl = get_template_module('events/sessions/management/_session_list.html')
    return tpl.render_session_list(event, **_get_session_list_args(event))


class RHSessionsList(RHManageSessionsBase):
    """Display list of all sessions within the event"""

    def _process(self):
        selected_entry = request.args.get('selected')
        selected_entry = int(selected_entry) if selected_entry else None
        return WPManageSessions.render_template('management/session_list.html', self.event,
                                                selected_entry=selected_entry,
                                                **_get_session_list_args(self.event))


class RHCreateSession(RHManageSessionsBase):
    """Create a session in the event"""

    def _get_response(self, new_session):
        sessions = [{'id': s.id, 'title': s.title, 'colors': s.colors} for s in self.event.sessions]
        return jsonify_data(sessions=sessions, new_session_id=new_session.id,
                            html=_render_session_list(self.event))

    def _process(self):
        inherited_location = self.event.location_data
        inherited_location['inheriting'] = True
        form = SessionForm(obj=FormDefaults(colors=get_random_color(self.event), location_data=inherited_location),
                           event=self.event)
        if form.validate_on_submit():
            new_session = create_session(self.event, form.data)
            return self._get_response(new_session)
        return jsonify_form(form)


class RHModifySession(RHManageSessionBase):
    """Modify a session"""

    def _process(self):
        form = SessionForm(obj=self.session, event=self.event)
        if form.validate_on_submit():
            update_session(self.session, form.data)
            return jsonify_data(html=_render_session_list(self.event))
        return jsonify_form(form)


class RHDeleteSessions(RHManageSessionsActionsBase):
    """Remove multiple sessions"""

    def _process(self):
        for sess in self.sessions:
            delete_session(sess)
        return jsonify_data(html=_render_session_list(self.event))


class RHManageSessionsExportBase(RHManageSessionsActionsBase):
    ALLOW_LOCKED = True


class RHExportSessionsCSV(RHManageSessionsExportBase):
    """Export list of sessions to a CSV"""

    def _process(self):
        headers, rows = generate_spreadsheet_from_sessions(self.sessions)
        return send_csv('sessions.csv', headers, rows)


class RHExportSessionsExcel(RHManageSessionsExportBase):
    """Export list of sessions to a XLSX"""

    def _process(self):
        headers, rows = generate_spreadsheet_from_sessions(self.sessions)
        return send_xlsx('sessions.xlsx', headers, rows)


class RHExportSessionsPDF(RHManageSessionsExportBase):
    """Export list of sessions to a PDF"""

    def _process(self):
        pdf_file = generate_pdf_from_sessions(self.sessions)
        return send_file('sessions.pdf', pdf_file, 'application/pdf')


class RHSessionREST(RHManageSessionBase):
    """Perform update or removal of a session"""

    def _process_DELETE(self):
        delete_session(self.session)
        return jsonify_data(html=_render_session_list(self.event))

    def _process_PATCH(self):
        data = request.json
        updates = {}
        if set(data.viewkeys()) > {'colors'}:
            raise BadRequest
        if 'colors' in data:
            colors = ColorTuple(**data['colors'])
            if colors not in get_colors():
                raise BadRequest
            updates['colors'] = colors
        update_session(self.session, updates)
        return jsonify()


class RHSessionPersonList(RHContributionPersonListMixin, RHManageSessionsActionsBase):
    """List of persons in the session's contributions"""

    template = 'events/sessions/management/session_person_list.html'
    ALLOW_LOCKED = True

    @property
    def _membership_filter(self):
        session_ids = {s.id for s in self.sessions}
        return Contribution.session_id.in_(session_ids)


class RHSessionProtection(RHManageSessionBase):
    """Manage session protection"""

    def _process(self):
        form = SessionProtectionForm(obj=FormDefaults(**self._get_defaults()), session=self.session,
                                     prefix='session-protection-')
        if form.validate_on_submit():
            update_session(self.session, {'protection_mode': form.protection_mode.data})
            if self.session.is_protected:
                update_object_principals(self.session, form.acl.data, read_access=True)
            update_object_principals(self.session, form.managers.data, full_access=True)
            update_object_principals(self.session, form.coordinators.data, role='coordinate')
            return jsonify_data(flash=False, html=_render_session_list(self.event))
        return jsonify_form(form)

    def _get_defaults(self):
        acl = {x.principal for x in self.session.acl_entries if x.read_access}
        managers = {x.principal for x in self.session.acl_entries if x.full_access}
        coordinators = {x.principal for x in self.session.acl_entries if x.has_management_role('coordinate',
                                                                                               explicit=True)}
        return {'managers': managers, 'protection_mode': self.session.protection_mode, 'coordinators': coordinators,
                'acl': acl}


class RHSessionACL(RHManageSessionBase):
    """Display the ACL of the session"""

    def _process(self):
        return render_acl(self.session)


class RHSessionACLMessage(RHManageSessionBase):
    """Render the inheriting ACL message"""

    def _process(self):
        mode = ProtectionMode[request.args['mode']]
        return jsonify_template('forms/protection_field_acl_message.html', object=self.session, mode=mode,
                                endpoint='sessions.acl')


class RHManageSessionBlock(RHManageSessionBase):
    """Manage a block of a session"""

    normalize_url_spec = {
        'locators': {
            lambda self: self.session_block
        }
    }

    def _process_args(self):
        RHManageSessionBase._process_args(self)
        self.session_block = SessionBlock.get_one(request.view_args['block_id'])

    def _process(self):
        form = MeetingSessionBlockForm(obj=FormDefaults(**self._get_form_defaults()), event=self.event,
                                       session_block=self.session_block)
        if form.validate_on_submit():
            session_data = {k[8:]: v for k, v in form.data.iteritems() if k in form.session_fields}
            block_data = {k[6:]: v for k, v in form.data.iteritems() if k in form.block_fields}
            update_session(self.session, session_data)
            update_session_block(self.session_block, block_data)
            return jsonify_data(flash=False)
        self.commit = False
        return jsonify_template('events/forms/session_block_form.html', form=form, block=self.session_block)

    def _get_form_defaults(self):
        fields = get_form_field_names(MeetingSessionBlockForm)
        defaults = {}
        defaults.update((name, getattr(self.session, name[8:])) for name in fields if name.startswith('session_'))
        defaults.update((name, getattr(self.session_block, name[6:])) for name in fields if name.startswith('block_'))
        return defaults


class RHSessionBlocks(RHManageSessionBase):
    def _process(self):
        return jsonify_template('events/sessions/management/session_blocks.html', sess=self.session)
