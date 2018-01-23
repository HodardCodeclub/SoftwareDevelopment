

from fossir.core.db import db
from fossir.util.serializer import Serializer
from fossir.util.string import return_ascii


class Aspect(db.Model, Serializer):
    __tablename__ = 'aspects'
    __table_args__ = {'schema': 'roombooking'}
    __public__ = ('id', 'name', 'center_latitude', 'center_longitude', 'zoom_level', 'top_left_latitude',
                  'top_left_longitude', 'bottom_right_latitude', 'bottom_right_longitude', 'default_on_startup')

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String,
        nullable=False
    )
    center_latitude = db.Column(
        db.String,
        nullable=False
    )
    center_longitude = db.Column(
        db.String,
        nullable=False
    )
    zoom_level = db.Column(
        db.SmallInteger,
        nullable=False
    )
    top_left_latitude = db.Column(
        db.String,
        nullable=False
    )
    top_left_longitude = db.Column(
        db.String,
        nullable=False
    )
    bottom_right_latitude = db.Column(
        db.String,
        nullable=False
    )
    bottom_right_longitude = db.Column(
        db.String,
        nullable=False
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('roombooking.locations.id'),
        nullable=False
    )

    # relationship backrefs:
    # - location (Location.aspects)

    @return_ascii
    def __repr__(self):
        return u'<Aspect({0}, {1}, {2})>'.format(
            self.id,
            self.location_id,
            self.name
        )

    @property
    def default_on_startup(self):
        return self.id == self.location.default_aspect_id
