

from __future__ import unicode_literals

from flask import has_request_context, request, session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.modules.attachments import Attachment, AttachmentFolder
from fossir.modules.networks.models.networks import IPNetworkGroup
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


logger = Logger.get('networks')


@signals.menu.items.connect_via('admin-sidemenu')
def _sidemenu_items(sender, **kwargs):
    if session.user.is_admin:
        yield SideMenuItem('ip_networks', _('IP Networks'), url_for('networks.manage'), section='security')


@signals.acl.can_access.connect_via(Attachment)
@signals.acl.can_access.connect_via(AttachmentFolder)
def _can_access(cls, obj, user, authorized, **kwargs):
    # Grant full access to attachments/folders to certain networks
    if not has_request_context() or not request.remote_addr or authorized is not None:
        return
    ip = unicode(request.remote_addr)
    if any(net.contains_ip(ip) for net in IPNetworkGroup.query.filter_by(attachment_access_override=True)):
        return True
