

from __future__ import unicode_literals

from flask import request
from sqlalchemy.orm import contains_eager, defaultload

from fossir.modules.events.management.controllers import RHManageEventBase
from fossir.modules.events.registration.controllers import RegistrationFormMixin
from fossir.modules.events.registration.lists import RegistrationListGenerator
from fossir.modules.events.registration.models.forms import RegistrationForm
from fossir.modules.events.registration.models.registrations import Registration


class RHManageRegFormsBase(RHManageEventBase):
    """Base class for all registration management RHs"""

    ROLE = 'registration'


class RHManageRegFormBase(RegistrationFormMixin, RHManageRegFormsBase):
    """Base class for a specific registration form"""

    def _process_args(self):
        RHManageRegFormsBase._process_args(self)
        RegistrationFormMixin._process_args(self)
        self.list_generator = RegistrationListGenerator(regform=self.regform)


class RHManageRegistrationBase(RHManageRegFormBase):
    """Base class for a specific registration"""

    normalize_url_spec = {
        'locators': {
            lambda self: self.registration
        }
    }

    def _process_args(self):
        RHManageRegFormBase._process_args(self)
        self.registration = (Registration
                             .find(Registration.id == request.view_args['registration_id'],
                                   ~Registration.is_deleted,
                                   ~RegistrationForm.is_deleted)
                             .join(Registration.registration_form)
                             .options(contains_eager(Registration.registration_form)
                                      .defaultload('form_items')
                                      .joinedload('children'))
                             .options(defaultload(Registration.data)
                                      .joinedload('field_data'))
                             .one())
