

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.core.roles import ManagementRole
from fossir.modules.events import Event
from fossir.modules.events.models.events import EventType
from fossir.modules.events.tracks.clone import TrackCloner
from fossir.modules.events.tracks.models.tracks import Track
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


logger = Logger.get('tracks')


@signals.menu.items.connect_via('event-management-sidemenu')
def _sidemenu_items(sender, event, **kwargs):
    if event.type_ == EventType.conference and event.can_manage(session.user):
        return SideMenuItem('program', _('Programme'), url_for('tracks.manage', event), section='organization')


@signals.event.sidemenu.connect
def _extend_event_menu(sender, **kwargs):
    from fossir.modules.events.layout.util import MenuEntryData
    from fossir.modules.events.tracks.settings import track_settings

    def _program_visible(event):
        return bool(track_settings.get(event, 'program').strip() or Track.query.with_parent(event).has_rows())

    return MenuEntryData(title=_("Scientific Programme"), name='program', endpoint='tracks.program', position=1,
                         visible=_program_visible, static_site=True)


@signals.users.merged.connect
def _merge_users(target, source, **kwargs):
    target.abstract_reviewer_for_tracks |= source.abstract_reviewer_for_tracks
    source.abstract_reviewer_for_tracks.clear()
    target.convener_for_tracks |= source.convener_for_tracks
    source.convener_for_tracks.clear()


@signals.event_management.get_cloners.connect
def _get_cloners(sender, **kwargs):
    yield TrackCloner


@signals.acl.get_management_roles.connect_via(Event)
def _get_management_roles(sender, **kwargs):
    return TrackConvenerRole


class TrackConvenerRole(ManagementRole):
    name = 'track_convener'
    friendly_name = _('Track convener')
    description = _('Grants track convener rights in an event')
