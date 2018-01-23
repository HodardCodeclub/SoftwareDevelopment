

from __future__ import unicode_literals

from flask import flash, redirect, request, session
from sqlalchemy.orm import defaultload

from fossir.modules.events.registration.models.forms import RegistrationForm
from fossir.modules.events.registration.util import get_event_section_data, make_registration_form, modify_registration
from fossir.util.string import camelize_keys


class RegistrationFormMixin:
    """Mixin for single registration form RH"""

    normalize_url_spec = {
        'locators': {
            lambda self: self.regform
        }
    }

    def _process_args(self):
        self.regform = (RegistrationForm.query
                        .filter_by(id=request.view_args['reg_form_id'], is_deleted=False)
                        .options(defaultload('form_items').joinedload('children').joinedload('current_data'))
                        .one())


class RegistrationEditMixin:
    def _process(self):
        form = make_registration_form(self.regform, management=self.management, registration=self.registration)()

        if form.validate_on_submit():
            data = form.data
            notify_user = not self.management or data.pop('notify_user', False)
            if self.management:
                session['registration_notify_user_default'] = notify_user
            modify_registration(self.registration, data, management=self.management, notify_user=notify_user)
            return redirect(self.success_url)
        elif form.is_submitted():
            # not very pretty but usually this never happens thanks to client-side validation
            for error in form.error_list:
                flash(error, 'error')

        registration_data = {r.field_data.field.html_field_name: camelize_keys(r.user_data)
                             for r in self.registration.data}
        section_data = camelize_keys(get_event_section_data(self.regform, management=self.management,
                                                            registration=self.registration))

        registration_metadata = {
            'paid': self.registration.is_paid,
            'manager': self.management
        }

        return self.view_class.render_template(self.template_file, self.event,
                                               sections=section_data, regform=self.regform,
                                               registration_data=registration_data,
                                               registration_metadata=registration_metadata,
                                               registration=self.registration)
