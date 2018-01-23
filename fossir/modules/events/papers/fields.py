

from __future__ import unicode_literals

import json

from fossir.modules.events.papers.settings import paper_reviewing_settings as settings
from fossir.modules.events.papers.settings import RoleConverter
from fossir.web.forms.fields import JSONField
from fossir.web.forms.widgets import JinjaWidget


class PaperEmailSettingsField(JSONField):
    CAN_POPULATE = True
    widget = JinjaWidget('events/papers/forms/paper_email_settings_widget.html')

    @property
    def event(self):
        return self.get_form().event

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = json.loads(valuelist[0])
            data = {}
            for key, value in self.data.iteritems():
                data[key] = RoleConverter.to_python(value) if isinstance(value, list) else value
            self.data = data

    def _value(self):
        return {
            'notify_on_added_to_event': [x.name for x in settings.get(self.event, 'notify_on_added_to_event')],
            'notify_on_assigned_contrib': [x.name for x in settings.get(self.event, 'notify_on_assigned_contrib')],
            'notify_on_paper_submission': [x.name for x in settings.get(self.event, 'notify_on_paper_submission')],
            'notify_judge_on_review': settings.get(self.event, 'notify_judge_on_review'),
            'notify_author_on_judgment': settings.get(self.event, 'notify_author_on_judgment')
        }
