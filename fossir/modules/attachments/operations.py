

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.db import db
from fossir.modules.attachments import logger
from fossir.modules.attachments.models.attachments import Attachment, AttachmentType
from fossir.modules.attachments.models.folders import AttachmentFolder


def add_attachment_link(data, linked_object):
    """Add a link attachment to linked_object"""
    folder = data.pop('folder', None)
    if not folder:
        folder = AttachmentFolder.get_or_create_default(linked_object=linked_object)
    assert folder.object == linked_object
    link = Attachment(user=session.user, type=AttachmentType.link, folder=folder)
    link.populate_from_dict(data, skip={'acl', 'protected'})
    if link.is_self_protected:
        link.acl = data['acl']
    db.session.flush()
    logger.info('Attachment %s added by %s', link, session.user)
    signals.attachments.attachment_created.send(link, user=session.user)
