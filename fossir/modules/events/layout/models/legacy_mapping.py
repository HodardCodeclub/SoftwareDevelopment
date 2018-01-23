

from __future__ import unicode_literals

from fossir.core.db import db
from fossir.util.string import format_repr, return_ascii


class LegacyImageMapping(db.Model):
    """Legacy image id mapping

    Legacy images had event-unique numeric ids. Using this
    mapping we can resolve old ones to their new id.
    """

    __tablename__ = 'legacy_image_id_map'
    __table_args__ = {'schema': 'events'}

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.events.id'),
        primary_key=True,
        index=True,
        autoincrement=False
    )
    legacy_image_id = db.Column(
        db.Integer,
        primary_key=True,
        index=True,
        autoincrement=False
    )
    image_id = db.Column(
        db.Integer,
        db.ForeignKey('events.image_files.id'),
        nullable=False,
        index=True
    )

    image = db.relationship(
        'ImageFile',
        lazy=False,
        backref=db.backref(
            'legacy_mapping',
            cascade='all, delete-orphan',
            uselist=False,
            lazy=True
        )
    )

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'legacy_image_id', 'image_id')


class LegacyPageMapping(db.Model):
    """Legacy page id mapping

    Legacy pages had event-unique numeric ids. Using this
    mapping we can resolve old ones to their new id.
    """

    __tablename__ = 'legacy_page_id_map'
    __table_args__ = {'schema': 'events'}

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.events.id'),
        primary_key=True,
        index=True,
        autoincrement=False
    )
    legacy_page_id = db.Column(
        db.Integer,
        primary_key=True,
        index=True,
        autoincrement=False
    )
    page_id = db.Column(
        db.Integer,
        db.ForeignKey('events.pages.id'),
        nullable=False,
        index=True
    )

    page = db.relationship(
        'EventPage',
        lazy=False,
        backref=db.backref(
            'legacy_mapping',
            cascade='all, delete-orphan',
            uselist=False,
            lazy=True
        )
    )

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'legacy_page_id', 'page_id')
