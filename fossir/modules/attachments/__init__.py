

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.modules.attachments.logging import connect_log_signals
from fossir.modules.attachments.models.attachments import Attachment
from fossir.modules.attachments.models.folders import AttachmentFolder
from fossir.modules.attachments.util import can_manage_attachments
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


logger = Logger.get('attachments')
connect_log_signals()


@signals.users.merged.connect
def _merge_users(target, source, **kwargs):
    from fossir.modules.attachments.models.attachments import Attachment, AttachmentFile
    from fossir.modules.attachments.models.principals import AttachmentPrincipal, AttachmentFolderPrincipal
    Attachment.find(user_id=source.id).update({Attachment.user_id: target.id})
    AttachmentFile.find(user_id=source.id).update({AttachmentFile.user_id: target.id})
    AttachmentPrincipal.merge_users(target, source, 'attachment')
    AttachmentFolderPrincipal.merge_users(target, source, 'folder')


@signals.menu.items.connect_via('event-management-sidemenu')
def _extend_event_management_menu(sender, event, **kwargs):
    if not can_manage_attachments(event, session.user):
        return
    return SideMenuItem('attachments', _('Materials'), url_for('attachments.management', event), 80,
                        section='organization')


@signals.event_management.management_url.connect
def _get_event_management_url(event, **kwargs):
    if can_manage_attachments(event, session.user):
        return url_for('attachments.management', event)


@signals.menu.items.connect_via('category-management-sidemenu')
def _extend_category_management_menu(sender, category, **kwargs):
    return SideMenuItem('attachments', _('Materials'), url_for('attachments.management', category), icon='upload')


@signals.event_management.get_cloners.connect
def _get_attachment_cloner(sender, **kwargs):
    from fossir.modules.attachments.clone import AttachmentCloner
    return AttachmentCloner
