

from __future__ import unicode_literals

from flask import request

from fossir.modules.events.management.controllers import RHManageEventBase
from fossir.modules.events.surveys.models.surveys import Survey


class RHManageSurveysBase(RHManageEventBase):
    """Base class for all survey management RHs"""

    ROLE = 'surveys'


class RHManageSurveyBase(RHManageSurveysBase):
    """Base class for specific survey management RHs."""

    normalize_url_spec = {
        'locators': {
            lambda self: self.survey
        }
    }

    def _process_args(self):
        RHManageSurveysBase._process_args(self)
        self.survey = Survey.find_one(id=request.view_args['survey_id'], is_deleted=False)
