

from __future__ import unicode_literals

from fossir.core import signals
from fossir.core.config import config
from fossir.core.db import db
from fossir.modules.users import User


def create_user(email, data, identity=None, settings=None, other_emails=None, from_moderation=True):
    """Create a new user.

    This may also convert a pending user to a proper user in case the
    email address matches such a user.

    :param email: The primary email address of the user.
    :param data: The data used to populate the user.
    :param identity: An `Identity` to associate with the user.
    :param settings: A dict containing user settings.
    :param other_emails: A set of email addresses that are also used
                         to check for a pending user. They will also
                         be added as secondary emails to the user.
    :param from_moderation: Whether the user was created through the
                            moderation process or manually by an admin.
    """
    if other_emails is None:
        other_emails = set()
    if settings is None:
        settings = {}
    settings.setdefault('timezone', config.DEFAULT_TIMEZONE)
    settings.setdefault('lang', config.DEFAULT_LOCALE)
    settings.setdefault('suggest_categories', False)
    # Get a pending user if there is one
    user = User.find_first(~User.is_deleted, User.is_pending,
                           User.all_emails.contains(db.func.any(list({email} | set(other_emails)))))
    if not user:
        user = User()

    if email in user.secondary_emails:
        # This can happen if there's a pending user who has a secondary email
        # for some weird reason which should now become the primary email...
        user.make_email_primary(email)
    else:
        user.email = email
    user.populate_from_dict(data)
    user.is_pending = False
    user.secondary_emails |= other_emails
    user.favorite_users.add(user)
    if identity is not None:
        user.identities.add(identity)
    db.session.add(user)
    user.settings.set_multi(settings)
    db.session.flush()
    signals.users.registered.send(user, from_moderation=from_moderation, identity=identity)
    db.session.flush()
    return user
