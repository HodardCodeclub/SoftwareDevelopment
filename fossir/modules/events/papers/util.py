

from __future__ import unicode_literals

from sqlalchemy.orm import load_only, noload

from fossir.core.db import db
from fossir.modules.events import Event
from fossir.modules.events.abstracts.models.abstracts import Abstract
from fossir.modules.events.contributions import Contribution
from fossir.modules.events.contributions.models.persons import ContributionPersonLink
from fossir.modules.events.models.principals import EventPrincipal
from fossir.modules.events.papers.models.revisions import PaperRevision, PaperRevisionState
from fossir.modules.users import User


def _query_contributions_with_user_as_reviewer(event, user):
    query = Contribution.query.with_parent(event)
    query = query.filter(db.or_(Contribution.paper_content_reviewers.any(User.id == user.id),
                                Contribution.paper_layout_reviewers.any(User.id == user.id)),
                         Contribution._paper_revisions.any())
    return query


def get_user_reviewed_contributions(event, user):
    """Get the list of contributions where user already reviewed paper"""
    contribs = _query_contributions_with_user_as_reviewer(event, user).all()
    contribs = [contrib for contrib in contribs if contrib.paper.last_revision.has_user_reviewed(user)]
    return contribs


def get_user_contributions_to_review(event, user):
    """Get the list of contributions where user has paper to review"""
    contribs = _query_contributions_with_user_as_reviewer(event, user).all()
    contribs = [contrib for contrib in contribs if not contrib.paper.last_revision.has_user_reviewed(user)]
    return contribs


def get_events_with_paper_roles(user, dt=None):
    """
    Get the IDs and PR roles of events where the user has any kind
    of paper reviewing privileges.

    :param user: A `User`
    :param dt: Only include events taking place on/after that date
    :return: A dict mapping event IDs to a set of roles
    """
    paper_roles = {'paper_manager', 'paper_judge', 'paper_content_reviewer', 'paper_layout_reviewer'}
    role_criteria = [EventPrincipal.has_management_role(role, explicit=True) for role in paper_roles]
    query = (user.in_event_acls
             .join(Event)
             .options(noload('user'), noload('local_group'), load_only('event_id', 'roles'))
             .filter(~Event.is_deleted, Event.ends_after(dt))
             .filter(db.or_(*role_criteria)))
    return {principal.event_id: set(principal.roles) & paper_roles for principal in query}


def get_contributions_with_paper_submitted_by_user(event, user):
    return (Contribution.query.with_parent(event)
            .filter(Contribution._paper_revisions.any(PaperRevision.submitter == user))
            .all())


def _query_contributions_with_user_paper_submission_rights(event, user):
    criteria = [Contribution.person_links.any(ContributionPersonLink.person.has(user=user)),
                Contribution.abstract.has(Abstract.submitter_id == user.id)]
    return Contribution.query.with_parent(event).filter(db.or_(*criteria))


def has_contributions_with_user_paper_submission_rights(event, user):
    return _query_contributions_with_user_paper_submission_rights(event, user).has_rows()


def get_user_submittable_contributions(event, user):
    criteria = [Contribution._paper_last_revision == None,  # noqa
                Contribution._paper_last_revision.has(PaperRevision.state == PaperRevisionState.to_be_corrected)]
    return (_query_contributions_with_user_paper_submission_rights(event, user)
            .filter(db.or_(*criteria))
            .all())
