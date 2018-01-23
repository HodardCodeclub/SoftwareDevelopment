

from fossir.core.db import db
from fossir.util.string import return_ascii


RoomEquipmentAssociation = db.Table(
    'room_equipment',
    db.metadata,
    db.Column(
        'equipment_id',
        db.Integer,
        db.ForeignKey('roombooking.equipment_types.id'),
        primary_key=True,
    ),
    db.Column(
        'room_id',
        db.Integer,
        db.ForeignKey('roombooking.rooms.id'),
        primary_key=True
    ),
    schema='roombooking'
)

ReservationEquipmentAssociation = db.Table(
    'reservation_equipment',
    db.metadata,
    db.Column(
        'equipment_id',
        db.Integer,
        db.ForeignKey('roombooking.equipment_types.id'),
        primary_key=True,
    ),
    db.Column(
        'reservation_id',
        db.Integer,
        db.ForeignKey('roombooking.reservations.id'),
        primary_key=True
    ),
    schema='roombooking'
)


class EquipmentType(db.Model):
    __tablename__ = 'equipment_types'
    __table_args__ = (db.UniqueConstraint('name', 'location_id'),
                      {'schema': 'roombooking'})

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('roombooking.equipment_types.id')
    )
    name = db.Column(
        db.String,
        nullable=False,
        index=True
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('roombooking.locations.id'),
        nullable=False
    )

    children = db.relationship(
        'EquipmentType',
        backref=db.backref(
            'parent',
            remote_side=[id]
        )
    )

    # relationship backrefs:
    # - location (Location.equipment_types)
    # - parent (EquipmentType.children)
    # - reservations (Reservation.used_equipment)
    # - rooms (Room.available_equipment)

    @return_ascii
    def __repr__(self):
        return u'<EquipmentType({0}, {1}, {2})>'.format(self.id, self.name, self.location_id)
