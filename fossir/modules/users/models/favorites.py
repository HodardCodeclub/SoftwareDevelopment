

from __future__ import unicode_literals

from fossir.core.db import db


favorite_user_table = db.Table(
    'favorite_users',
    db.metadata,
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.users.id'),
        primary_key=True,
        nullable=False,
        index=True
    ),
    db.Column(
        'target_id',
        db.Integer,
        db.ForeignKey('users.users.id'),
        primary_key=True,
        nullable=False,
        index=True
    ),
    schema='users'
)

favorite_category_table = db.Table(
    'favorite_categories',
    db.metadata,
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.users.id'),
        primary_key=True,
        nullable=False,
        index=True
    ),
    db.Column(
        'target_id',
        db.Integer,
        db.ForeignKey('categories.categories.id'),
        primary_key=True,
        nullable=False,
        index=True
    ),
    schema='users'
)
