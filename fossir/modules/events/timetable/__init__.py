

from __future__ import unicode_literals

from flask import render_template, session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.modules.events.timetable.models.entries import TimetableEntry, TimetableEntryType
from fossir.util.date_time import now_utc
from fossir.util.i18n import _
from fossir.web.flask.templating import template_hook
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


logger = Logger.get('events.timetable')


@signals.event.sidemenu.connect
def _extend_event_menu(sender, **kwargs):
    from fossir.modules.events.layout.util import MenuEntryData
    yield MenuEntryData(title=_("Timetable"), name='timetable', endpoint='timetable.timetable', position=3,
                        static_site=True)


@signals.menu.items.connect_via('event-management-sidemenu')
def _extend_event_management_menu(sender, event, **kwargs):
    from fossir.modules.events.sessions.util import can_manage_sessions
    if not can_manage_sessions(session.user, event, 'ANY'):
        return
    if event.type != 'lecture':
        return SideMenuItem('timetable', _('Timetable'), url_for('timetable.management', event), weight=80,
                            icon='calendar')


@signals.event_management.get_cloners.connect
def _get_timetable_cloner(sender, **kwargs):
    from fossir.modules.events.timetable.clone import TimetableCloner
    return TimetableCloner


@template_hook('session-timetable')
def _render_session_timetable(session, **kwargs):
    from fossir.modules.events.timetable.util import render_session_timetable
    return render_session_timetable(session, **kwargs)


@template_hook('now-happening')
def _render_now_happening_info(event, text_color_css, **kwargs):
    from fossir.modules.events.layout import layout_settings
    if layout_settings.get(event, 'show_banner'):
        current_dt = now_utc(exact=False)
        entries = event.timetable_entries.filter(TimetableEntry.start_dt <= current_dt,
                                                 TimetableEntry.end_dt > current_dt,
                                                 TimetableEntry.type != TimetableEntryType.SESSION_BLOCK).all()
        if not entries:
            return
        return render_template('events/display/now_happening.html', event=event, entries=entries,
                               text_color_css=text_color_css)
