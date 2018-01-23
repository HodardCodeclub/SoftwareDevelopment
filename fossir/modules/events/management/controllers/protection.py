

from __future__ import unicode_literals

from flask import flash, redirect, request
from werkzeug.exceptions import NotFound

from fossir.core.db.sqlalchemy.protection import ProtectionMode, render_acl
from fossir.modules.events.management.controllers.base import RHManageEventBase
from fossir.modules.events.management.forms import EventProtectionForm
from fossir.modules.events.management.views import WPEventProtection
from fossir.modules.events.operations import update_event_protection
from fossir.modules.events.sessions import COORDINATOR_PRIV_SETTINGS, session_settings
from fossir.modules.events.sessions.operations import update_session_coordinator_privs
from fossir.modules.events.util import get_object_from_args, update_object_principals
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import FormDefaults
from fossir.web.util import jsonify_template


class RHShowNonInheriting(RHManageEventBase):
    """Show a list of non-inheriting child objects"""

    def _process_args(self):
        RHManageEventBase._process_args(self)
        self.obj = get_object_from_args()[2]
        if self.obj is None:
            raise NotFound

    def _process(self):
        objects = self.obj.get_non_inheriting_objects()
        return jsonify_template('events/management/non_inheriting_objects.html', objects=objects)


class RHEventACL(RHManageEventBase):
    """Display the inherited ACL of the event"""

    def _process(self):
        return render_acl(self.event)


class RHEventACLMessage(RHManageEventBase):
    """Render the inheriting ACL message"""

    def _process(self):
        mode = ProtectionMode[request.args['mode']]
        return jsonify_template('forms/protection_field_acl_message.html', object=self.event, mode=mode,
                                endpoint='event_management.acl')


class RHEventProtection(RHManageEventBase):
    """Show event protection"""

    NOT_SANITIZED_FIELDS = {'access_key'}

    def _process(self):
        form = EventProtectionForm(obj=FormDefaults(**self._get_defaults()), event=self.event)
        if form.validate_on_submit():
            update_event_protection(self.event, {'protection_mode': form.protection_mode.data,
                                                     'own_no_access_contact': form.own_no_access_contact.data,
                                                     'access_key': form.access_key.data,
                                                     'visibility': form.visibility.data})
            update_object_principals(self.event, form.acl.data, read_access=True)
            update_object_principals(self.event, form.managers.data, full_access=True)
            update_object_principals(self.event, form.submitters.data, role='submit')
            self._update_session_coordinator_privs(form)
            flash(_('Protection settings have been updated'), 'success')
            return redirect(url_for('.protection', self.event))
        return WPEventProtection.render_template('event_protection.html', self.event, 'protection', form=form)

    def _get_defaults(self):
        acl = {p.principal for p in self.event.acl_entries if p.read_access}
        submitters = {p.principal for p in self.event.acl_entries if p.has_management_role('submit', explicit=True)}
        managers = {p.principal for p in self.event.acl_entries if p.full_access}
        registration_managers = {p.principal for p in self.event.acl_entries
                                 if p.has_management_role('registration', explicit=True)}
        event_session_settings = session_settings.get_all(self.event)
        coordinator_privs = {name: event_session_settings[val] for name, val in COORDINATOR_PRIV_SETTINGS.iteritems()
                             if event_session_settings.get(val)}
        return dict({'protection_mode': self.event.protection_mode, 'acl': acl, 'managers': managers,
                     'registration_managers': registration_managers, 'submitters': submitters,
                     'access_key': self.event.access_key, 'visibility': self.event.visibility,
                     'own_no_access_contact': self.event.own_no_access_contact}, **coordinator_privs)

    def _update_session_coordinator_privs(self, form):
        data = {field: getattr(form, field).data for field in form.priv_fields}
        update_session_coordinator_privs(self.event, data)
