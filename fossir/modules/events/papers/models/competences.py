

from __future__ import unicode_literals

from sqlalchemy import ARRAY

from fossir.core.db import db
from fossir.util.string import format_repr, return_ascii


class PaperCompetence(db.Model):
    __tablename__ = 'competences'
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id'),
                      {'schema': 'event_paper_reviewing'})

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.users.id'),
        index=True,
        nullable=False
    )
    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.events.id'),
        index=True,
        nullable=False
    )
    competences = db.Column(
        ARRAY(db.String),
        nullable=False,
        default=[]
    )

    event = db.relationship(
        'Event',
        lazy=True,
        backref=db.backref(
            'paper_competences',
            cascade='all, delete-orphan',
            lazy=True
        )
    )
    user = db.relationship(
        'User',
        lazy=True,
        backref=db.backref(
            'paper_competences',
            lazy='dynamic'
        )
    )

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'id', 'user_id', 'event_id', _text=', '.join(self.competences))
