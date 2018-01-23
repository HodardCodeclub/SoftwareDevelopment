

from __future__ import unicode_literals

import posixpath

from fossir.core.config import config
from fossir.core.db import db
from fossir.core.storage import StoredFileMixin
from fossir.util.string import return_ascii, strict_unicode


class ImageFile(StoredFileMixin, db.Model):
    __tablename__ = 'image_files'
    __table_args__ = {'schema': 'events'}

    # Image files are not version-controlled
    version_of = None

    #: The ID of the file
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    #: The event the image belongs to
    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.events.id'),
        nullable=False,
        index=True
    )

    event = db.relationship(
        'Event',
        lazy=False,
        backref=db.backref(
            'layout_images',
            lazy='dynamic'
        )
    )

    # relationship backrefs:
    # - legacy_mapping (LegacyImageMapping.image)

    @property
    def locator(self):
        return dict(self.event.locator, image_id=self.id, filename=self.filename)

    def _build_storage_path(self):
        path_segments = ['event', strict_unicode(self.event.id), 'images']
        self.assign_id()
        filename = '{}-{}'.format(self.id, self.filename)
        path = posixpath.join(*(path_segments + [filename]))
        return config.ATTACHMENT_STORAGE, path

    @return_ascii
    def __repr__(self):
        return '<ImageFile({}, {}, {}, {})>'.format(
            self.id,
            self.event_id,
            self.filename,
            self.content_type
        )
