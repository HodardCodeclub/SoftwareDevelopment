

from __future__ import unicode_literals

from flask import request
from werkzeug.exceptions import NotFound

from fossir.modules.attachments.models.attachments import Attachment, AttachmentType
from fossir.modules.attachments.models.folders import AttachmentFolder


class SpecificAttachmentMixin:
    """Mixin for RHs that reference a specific attachment"""

    normalize_url_spec = {
        'args': {
            'folder_id': lambda self: self.attachment.folder_id,
            'filename': lambda self: (self.attachment.file.filename if self.attachment.type == AttachmentType.file
                                      else 'go')
        },
        'locators': {
            lambda self: self.attachment.folder.object
        },
        'preserved_args': {'attachment_id'}
    }

    def _process_args(self):
        self.attachment = Attachment.find_one(id=request.view_args['attachment_id'], is_deleted=False)
        if self.attachment.folder.is_deleted:
            raise NotFound


class SpecificFolderMixin:
    """Mixin for RHs that reference a specific folder"""

    normalize_url_spec = {
        'locators': {
            lambda self: self.folder.object
        },
        'preserved_args': {'folder_id'}
    }

    def _process_args(self):
        self.folder = AttachmentFolder.find_one(id=request.view_args['folder_id'], is_deleted=False)
