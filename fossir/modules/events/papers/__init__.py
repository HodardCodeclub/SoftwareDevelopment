
from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.core.roles import ManagementRole
from fossir.modules.events.features.base import EventFeature
from fossir.modules.events.models.events import Event, EventType
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


logger = Logger.get('events.papers')


@signals.menu.items.connect_via('event-management-sidemenu')
def _extend_event_management_menu(sender, event, **kwargs):
    if not event.cfp.is_manager(session.user) or not PapersFeature.is_allowed_for_event(event):
        return
    return SideMenuItem('papers', _('Call for Papers'), url_for('papers.management', event),
                        section='organization')


@signals.event_management.management_url.connect
def _get_event_management_url(event, **kwargs):
    if event.cfp.is_manager(session.user):
        return url_for('papers.management', event)


@signals.event.get_feature_definitions.connect
def _get_feature_definitions(sender, **kwargs):
    return PapersFeature


@signals.acl.get_management_roles.connect_via(Event)
def _get_management_roles(sender, **kwargs):
    yield PaperManagerRole
    yield PaperJudgeRole
    yield PaperContentReviewerRole
    yield PaperLayoutReviewerRole


class PapersFeature(EventFeature):
    name = 'papers'
    friendly_name = _('Call for Papers')
    description = _('Gives event managers the opportunity to open a "Call for Papers" and use the paper '
                    'reviewing workflow.')

    @classmethod
    def is_allowed_for_event(cls, event):
        return event.type_ == EventType.conference


class PaperManagerRole(ManagementRole):
    name = 'paper_manager'
    friendly_name = _('Paper Manager')
    description = _('Grants management rights for paper reviewing on an event.')


class PaperJudgeRole(ManagementRole):
    name = 'paper_judge'
    friendly_name = _('Judge')
    description = _('Grants paper judgment rights for assigned papers.')


class PaperContentReviewerRole(ManagementRole):
    name = 'paper_content_reviewer'
    friendly_name = _('Content reviewer')
    description = _('Grants content reviewing rights for assigned papers.')


class PaperLayoutReviewerRole(ManagementRole):
    name = 'paper_layout_reviewer'
    friendly_name = _('Layout reviewer')
    description = _('Grants layout reviewing rights for assigned papers.')


@signals.event.sidemenu.connect
def _extend_event_menu(sender, **kwargs):
    from fossir.modules.events.layout.util import MenuEntryData

    def _judging_area_visible(event):
        if not session.user or not event.has_feature('papers'):
            return False
        return event.cfp.can_access_judging_area(session.user)

    def _reviewing_area_visible(event):
        if not session.user or not event.has_feature('papers'):
            return False
        return event.cfp.can_access_reviewing_area(session.user)

    def _call_for_papers_visible(event):
        from fossir.modules.events.papers.util import has_contributions_with_user_paper_submission_rights
        if not session.user or not event.has_feature('papers'):
            return False
        return (has_contributions_with_user_paper_submission_rights(event, session.user) or
                event.cfp.is_staff(session.user))

    yield MenuEntryData(title=_("Call for Papers"), name='call_for_papers',
                        endpoint='papers.call_for_papers', position=8,
                        visible=_call_for_papers_visible)

    yield MenuEntryData(title=_("Reviewing Area"), name='paper_reviewing_area', parent='call_for_papers',
                        endpoint='papers.reviewing_area', position=0, visible=_reviewing_area_visible)

    yield MenuEntryData(title=_("Judging Area"), name='paper_judging_area', parent='call_for_papers',
                        endpoint='papers.papers_list', position=1, visible=_judging_area_visible)
