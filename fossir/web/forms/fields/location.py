

from __future__ import absolute_import, unicode_literals

from sqlalchemy.orm import joinedload

from fossir.core.db import db
from fossir.modules.rb import Location, Room
from fossir.web.forms.fields import JSONField
from fossir.web.forms.widgets import LocationWidget


class fossirLocationField(JSONField):
    CAN_POPULATE = True
    widget = LocationWidget()

    def __init__(self, *args, **kwargs):
        self.allow_location_inheritance = kwargs.pop('allow_location_inheritance', True)
        self.locations = Location.query.options(joinedload('rooms')).order_by(db.func.lower(Location.name)).all()
        super(fossirLocationField, self).__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        super(fossirLocationField, self).process_formdata(valuelist)
        self.data['room'] = Room.get(int(self.data['room_id'])) if self.data.get('room_id') else None
        self.data['venue'] = Location.get(int(self.data['venue_id'])) if self.data.get('venue_id') else None
        self.data['source'] = self.object_data.get('source') if self.object_data else None

    def _value(self):
        if not self.data:
            return {}
        result = {
            'address': self.data.get('address', ''),
            'inheriting': self.data.get('inheriting', False),
        }
        if self.data.get('room'):
            result['room_id'] = self.data['room'].id
            result['room_name'] = self.data['room'].full_name
            result['venue_id'] = self.data['room'].location.id
            result['venue_name'] = self.data['room'].location.name
        elif self.data.get('room_name'):
            result['room_name'] = self.data['room_name']
        if self.data.get('venue'):
            result['venue_id'] = self.data['venue'].id
            result['venue_name'] = self.data['venue'].name
        elif self.data.get('venue_name'):
            result['venue_name'] = self.data['venue_name']
        return result
