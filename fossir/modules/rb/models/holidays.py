

from fossir.core.db import db
from fossir.util.string import return_ascii


class Holiday(db.Model):
    __tablename__ = 'holidays'
    __table_args__ = (db.UniqueConstraint('date', 'location_id'),
                      {'schema': 'roombooking'})

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    date = db.Column(
        db.Date,
        nullable=False,
        index=True
    )
    name = db.Column(
        db.String
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('roombooking.locations.id'),
        nullable=False
    )

    # relationship backrefs:
    # - location (Location.holidays)

    @return_ascii
    def __repr__(self):
        return u'<Holiday({}, {}, {}, {})>'.format(self.id, self.date, self.name or 'n/a', self.location.name)
