

from fossir.modules.events.contributions.views import WPAuthorList, WPContributions, WPSpeakerList
from fossir.modules.events.layout.views import WPPage
from fossir.modules.events.registration.views import WPDisplayRegistrationParticipantList
from fossir.modules.events.sessions.views import WPDisplaySession
from fossir.modules.events.timetable.views import WPDisplayTimetable
from fossir.modules.events.tracks.views import WPDisplayTracks
from fossir.modules.events.views import WPConferenceDisplay, WPSimpleEventDisplay


class WPStaticEventBase:
    def _getHeader(self):
        return ""

    def _getFooter(self):
        return ""


class WPStaticSimpleEventDisplay(WPStaticEventBase, WPSimpleEventDisplay):
    pass


class WPStaticConferenceDisplay(WPStaticEventBase, WPConferenceDisplay):
    pass


class WPStaticTimetable(WPStaticEventBase, WPDisplayTimetable):
    endpoint = 'timetable.timetable'
    menu_entry_name = 'timetable'


class WPStaticConferenceProgram(WPStaticEventBase, WPDisplayTracks):
    endpoint = 'tracks.program'


class WPStaticDisplayRegistrationParticipantList(WPStaticEventBase, WPDisplayRegistrationParticipantList):
    endpoint = 'event_registration.participant_list'


class WPStaticContributionList(WPStaticEventBase, WPContributions):
    endpoint = 'contributions.contribution_list'
    template_prefix = 'events/contributions/'
    menu_entry_name = 'contributions'


class WPStaticCustomPage(WPStaticEventBase, WPPage):
    pass


class WPStaticAuthorList(WPStaticEventBase, WPAuthorList):
    endpoint = 'contributions.author_list'
    template_prefix = 'events/contributions/'
    menu_entry_name = 'author_index'


class WPStaticSpeakerList(WPStaticEventBase, WPSpeakerList):
    endpoint = 'contributions.speaker_list'
    template_prefix = 'events/contributions/'
    menu_entry_name = 'speaker_index'


class WPStaticSessionDisplay(WPStaticEventBase, WPDisplaySession):
    endpoint = 'sessions.display_session'


class WPStaticContributionDisplay(WPStaticEventBase, WPContributions):
    endpoint = 'contributions.display_contribution'


class WPStaticSubcontributionDisplay(WPStaticEventBase, WPContributions):
    endpoint = 'contributions.display_subcontribution'
