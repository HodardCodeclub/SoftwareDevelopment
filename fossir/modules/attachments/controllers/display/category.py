

from __future__ import unicode_literals

from fossir.modules.attachments.controllers.display.base import DownloadAttachmentMixin
from fossir.modules.categories.controllers.base import RHDisplayCategoryBase


class RHDownloadCategoryAttachment(DownloadAttachmentMixin, RHDisplayCategoryBase):
    def _process_args(self):
        RHDisplayCategoryBase._process_args(self)
        DownloadAttachmentMixin._process_args(self)
