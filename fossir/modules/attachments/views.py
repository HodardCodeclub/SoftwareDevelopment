

from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase, WPSimpleEventDisplayBase
from fossir.web.views import WPJinjaMixin


class AttachmentsMixin(WPJinjaMixin):
    template_prefix = 'attachments/'
    base_wp = None

    def _getPageContent(self, params):
        return WPJinjaMixin._getPageContent(self, params)


class WPEventAttachments(AttachmentsMixin, WPEventManagement):
    base_wp = WPEventManagement
    sidemenu_option = 'attachments'
    ALLOW_JSON = True


class WPEventFolderDisplay(WPSimpleEventDisplayBase, WPJinjaMixin):
    template_prefix = 'attachments/'

    def _getBody(self, params):
        return WPJinjaMixin._getPageContent(self, params)


class WPPackageEventAttachmentsManagement(WPEventAttachments, WPJinjaMixin):
    template_prefix = 'attachments/'

    def _getTabContent(self, params):
        return WPJinjaMixin._getPageContent(self, params)


class WPPackageEventAttachmentsDisplayConference(WPConferenceDisplayBase):
    template_prefix = 'attachments/'


class WPPackageEventAttachmentsDisplay(WPSimpleEventDisplayBase, WPJinjaMixin):
    template_prefix = 'attachments/'

    def _getBody(self, params):
        return WPJinjaMixin._getPageContent(self, params)
