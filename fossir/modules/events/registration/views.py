
from __future__ import unicode_literals

from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.models.events import EventType
from fossir.modules.events.views import WPConferenceDisplayBase, WPSimpleEventDisplayBase
from fossir.web.views import WPJinjaMixin


class WPManageRegistration(WPEventManagement):
    template_prefix = 'events/registration/'

    def __init__(self, rh, event_, active_menu_item=None, **kwargs):
        self.regform = kwargs.get('regform')
        self.registration = kwargs.get('registration')
        WPEventManagement.__init__(self, rh, event_, active_menu_item, **kwargs)

    @property
    def sidemenu_option(self):
        if self.event.type_ != EventType.conference:
            regform = self.regform
            if not regform:
                if self.registration:
                    regform = self.registration.registration_form
            if regform and regform.is_participation:
                return 'participants'
        return 'registration'

    def getJSFiles(self):
        return WPEventManagement.getJSFiles(self) + self._asset_env['modules_registration_js'].urls()


class WPManageRegistrationStats(WPManageRegistration):
    def getJSFiles(self):
        return (WPManageRegistration.getJSFiles(self) +
                self._asset_env['statistics_js'].urls() +
                self._includeJSPackage('jqplot_js', prefix=''))


class WPManageParticipants(WPManageRegistration):
    sidemenu_option = 'participants'


class DisplayRegistrationFormMixin(WPJinjaMixin):
    template_prefix = 'events/registration/'
    base_class = None

    def _getBody(self, params):
        return WPJinjaMixin._getPageContent(self, params)

    def getJSFiles(self):
        return self.base_class.getJSFiles(self) + self._asset_env['modules_registration_js'].urls()


class WPDisplayRegistrationFormConference(DisplayRegistrationFormMixin, WPConferenceDisplayBase):
    template_prefix = 'events/registration/'
    base_class = WPConferenceDisplayBase
    menu_entry_name = 'registration'


class WPDisplayRegistrationParticipantList(WPDisplayRegistrationFormConference):
    menu_entry_name = 'participants'


class WPDisplayRegistrationFormSimpleEvent(DisplayRegistrationFormMixin, WPSimpleEventDisplayBase):
    template_prefix = 'events/registration/'
    base_class = WPSimpleEventDisplayBase
