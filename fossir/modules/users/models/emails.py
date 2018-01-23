

from __future__ import unicode_literals

from fossir.core.db import db
from fossir.core.db.sqlalchemy.custom.unaccent import define_unaccented_lowercase_index
from fossir.util.string import return_ascii


class UserEmail(db.Model):
    __tablename__ = 'emails'
    __table_args__ = (db.CheckConstraint('email = lower(email)', 'lowercase_email'),
                      db.Index(None, 'email', unique=True, postgresql_where=db.text('NOT is_user_deleted')),
                      db.Index(None, 'user_id', unique=True,
                               postgresql_where=db.text('is_primary AND NOT is_user_deleted')),
                      {'schema': 'users'})

    #: the unique id of the email address
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #: the id of the associated user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.users.id'),
        nullable=False,
        index=True
    )
    #: the email address
    email = db.Column(
        db.String,
        nullable=False,
        index=True
    )
    #: if the email is the user's primary email
    is_primary = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    #: if the user is marked as deleted (e.g. due to a merge). DO NOT use this flag when actually deleting an email
    is_user_deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # relationship backrefs:
    # - user (User._all_emails)

    @return_ascii
    def __repr__(self):
        return '<UserEmail({}, {}, {})>'.format(self.id, self.email, self.is_primary, self.user)


define_unaccented_lowercase_index(UserEmail.email)
