

from __future__ import unicode_literals

from flask import redirect, request, session
from werkzeug.exceptions import Forbidden

from fossir.modules.attachments.controllers.display.base import DownloadAttachmentMixin
from fossir.modules.attachments.controllers.event_package import AttachmentPackageMixin
from fossir.modules.attachments.controllers.util import SpecificFolderMixin
from fossir.modules.attachments.views import (WPEventFolderDisplay, WPPackageEventAttachmentsDisplay,
                                              WPPackageEventAttachmentsDisplayConference)
from fossir.modules.events.controllers.base import RHDisplayEventBase, RHEventBase
from fossir.modules.events.models.events import EventType


class RHDownloadEventAttachment(DownloadAttachmentMixin, RHEventBase):
    def _process_args(self):
        RHEventBase._process_args(self)
        DownloadAttachmentMixin._process_args(self)


class RHListEventAttachmentFolder(SpecificFolderMixin, RHDisplayEventBase):
    def _process_args(self):
        RHDisplayEventBase._process_args(self)
        SpecificFolderMixin._process_args(self)

    def _check_access(self):
        RHDisplayEventBase._check_access(self)
        if not self.folder.can_access(session.user):
            raise Forbidden

    def _process(self):
        if request.args.get('redirect_if_single') == '1' and len(self.folder.attachments) == 1:
            return redirect(self.folder.attachments[0].download_url)

        return WPEventFolderDisplay.render_template('folder.html', self.event, folder=self.folder)


class RHPackageEventAttachmentsDisplay(AttachmentPackageMixin, RHDisplayEventBase):
    @property
    def wp(self):
        if self.event.type_ == EventType.conference:
            return WPPackageEventAttachmentsDisplayConference
        else:
            return WPPackageEventAttachmentsDisplay
