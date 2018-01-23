

from __future__ import unicode_literals

from fossir.modules.events.fields import PersonLinkListFieldBase
from fossir.modules.events.sessions.models.persons import SessionBlockPersonLink
from fossir.modules.events.util import serialize_person_link
from fossir.web.forms.widgets import JinjaWidget


class SessionBlockPersonLinkListField(PersonLinkListFieldBase):
    person_link_cls = SessionBlockPersonLink
    linked_object_attr = 'session_block'
    widget = JinjaWidget('events/sessions/forms/session_person_link_widget.html')

    def _serialize_person_link(self, principal, extra_data=None):
        extra_data = extra_data or {}
        return dict(extra_data, **serialize_person_link(principal))

    def _convert_data(self, data):
        return list({self._get_person_link(x) for x in data})
