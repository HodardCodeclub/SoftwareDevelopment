

from __future__ import unicode_literals

from fossir.core.db import db
from fossir.core.db.sqlalchemy import UTCDateTime
from fossir.util.date_time import now_utc
from fossir.util.locators import locator_property
from fossir.util.string import format_repr, return_ascii


class NewsItem(db.Model):
    __tablename__ = 'news'
    __table_args__ = {'schema': 'fossir'}

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    created_dt = db.Column(
        UTCDateTime,
        nullable=False,
        default=now_utc
    )
    title = db.Column(
        db.String,
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False
    )

    @locator_property
    def locator(self):
        return {'news_id': self.id}

    @locator.anchor_only
    def locator(self):
        return {'_anchor': self.anchor}

    @property
    def anchor(self):
        return 'news-{}'.format(self.id)

    @return_ascii
    def __repr__(self):
        return format_repr(self, 'id', _text=self.title)
