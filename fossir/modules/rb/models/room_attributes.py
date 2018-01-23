

from sqlalchemy.dialects.postgresql import JSON

from fossir.core.db import db
from fossir.util.string import return_ascii


class RoomAttributeAssociation(db.Model):
    __tablename__ = 'room_attribute_values'
    __table_args__ = {'schema': 'roombooking'}

    attribute_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'roombooking.room_attributes.id',
        ),
        primary_key=True
    )
    room_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'roombooking.rooms.id',
        ),
        primary_key=True
    )
    value = db.Column(
        JSON
    )

    attribute = db.relationship(
        'RoomAttribute',
        backref=db.backref(
            'room_associations',
            cascade='all, delete-orphan'
        )
    )

    # relationship backrefs:
    # - room (Room.attributes)

    @return_ascii
    def __repr__(self):
        return u'<RoomAttributeAssociation({0}, {1}, {2})>'.format(self.room_id, self.attribute.name, self.value)


class RoomAttribute(db.Model):
    __tablename__ = 'room_attributes'
    __table_args__ = (db.UniqueConstraint('name', 'location_id'),
                      {'schema': 'roombooking'})

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('roombooking.room_attributes.id')
    )
    name = db.Column(
        db.String,
        nullable=False,
        index=True
    )
    title = db.Column(
        db.String,
        nullable=False
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('roombooking.locations.id'),
        nullable=False
    )
    type = db.Column(
        db.String,
        nullable=False
    )
    is_required = db.Column(
        db.Boolean,
        nullable=False
    )
    is_hidden = db.Column(
        db.Boolean,
        nullable=False
    )

    children = db.relationship(
        'RoomAttribute',
        backref=db.backref(
            'parent',
            remote_side=[id]
        )
    )

    # relationship backrefs:
    # - location (Location.attributes)
    # - parent (RoomAttribute.children)
    # - room_associations (RoomAttributeAssociation.attribute)

    @return_ascii
    def __repr__(self):
        return u'<RoomAttribute({}, {}, {})>'.format(self.id, self.name, self.location.name)
