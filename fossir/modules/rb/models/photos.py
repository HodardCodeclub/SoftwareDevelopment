

from fossir.core.db import db
from fossir.util.string import return_ascii


class Photo(db.Model):
    __tablename__ = 'photos'
    __table_args__ = {'schema': 'roombooking'}

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    thumbnail = db.Column(
        db.LargeBinary,
        nullable=True
    )
    data = db.Column(
        db.LargeBinary,
        nullable=True
    )

    # relationship backrefs:
    # - room (Room.photo)

    @return_ascii
    def __repr__(self):
        return u'<Photo({0})>'.format(self.id)
