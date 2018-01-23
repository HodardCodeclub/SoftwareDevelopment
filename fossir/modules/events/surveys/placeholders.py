

from __future__ import unicode_literals

from markupsafe import Markup, escape

from fossir.util.i18n import _
from fossir.util.placeholders import Placeholder
from fossir.web.flask.util import url_for


class EventTitlePlaceholder(Placeholder):
    name = 'event_title'
    description = _("The title of the event")

    @classmethod
    def render(cls, event, survey, **kwargs):
        return event.title


class SurveyTitlePlaceholder(Placeholder):
    name = 'survey_title'
    description = _("The title of the survey")

    @classmethod
    def render(cls, event, survey, **kwargs):
        return survey.title


class SurveyLinkPlaceholder(Placeholder):
    name = 'survey_link'
    description = _("Link to the survey")
    required = True

    @classmethod
    def render(cls, event, survey, **kwargs):
        url = url_for('.display_survey_form', survey, survey.locator.token, _external=True)
        return Markup('<a href="{url}" title="{title}">{url}</a>'.format(url=url, title=escape(survey.title)))
