

from __future__ import unicode_literals

from flask import redirect, request, session
from werkzeug.exceptions import BadRequest, Forbidden

from fossir.core import signals
from fossir.core.errors import NoReportError
from fossir.modules.attachments.controllers.util import SpecificAttachmentMixin
from fossir.modules.attachments.models.attachments import AttachmentType
from fossir.modules.attachments.preview import get_file_previewer
from fossir.util.i18n import _
from fossir.web.util import jsonify_template


class DownloadAttachmentMixin(SpecificAttachmentMixin):
    """Download an attachment"""

    def _check_access(self):
        if not self.attachment.can_access(session.user):
            raise Forbidden

    def _process(self):
        from_preview = request.args.get('from_preview') == '1'
        force_download = request.args.get('download') == '1'

        signals.attachments.attachment_accessed.send(self.attachment, user=session.user, from_preview=from_preview)
        if request.values.get('preview') == '1':
            if self.attachment.type != AttachmentType.file:
                raise BadRequest
            previewer = get_file_previewer(self.attachment.file)
            if not previewer:
                raise NoReportError.wrap_exc(BadRequest(_('There is no preview available for this file type. '
                                                          'Please refresh the page.')))
            preview_content = previewer.generate_content(self.attachment)
            return jsonify_template('attachments/preview.html', attachment=self.attachment,
                                    preview_content=preview_content)
        else:
            if self.attachment.type == AttachmentType.link:
                return redirect(self.attachment.link_url)
            else:
                return self.attachment.file.send(inline=not force_download)
