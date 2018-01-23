

from __future__ import unicode_literals

from fossir.core.marshmallow import mm
from fossir.modules.events.tracks.models.tracks import Track


class TrackSchema(mm.ModelSchema):
    class Meta:
        model = Track
        fields = ('id', 'title', 'code', 'description')


track_schema = TrackSchema()
track_schema_basic = TrackSchema(only=('id', 'title', 'code'))
