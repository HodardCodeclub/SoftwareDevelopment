.

from __future__ import unicode_literals

from collections import defaultdict

from flask import session
from werkzeug.exceptions import Forbidden

from fossir.modules.events.contributions.models.persons import (AuthorType, ContributionPersonLink,
                                                                SubContributionPersonLink)
from fossir.modules.events.contributions.models.subcontributions import SubContribution
from fossir.modules.events.controllers.base import RHEventBase
from fossir.modules.events.util import check_event_locked
from fossir.util.i18n import _
from fossir.web.util import jsonify_template


class ManageEventMixin(object):
    ALLOW_LOCKED = False
    ROLE = None

    def _require_user(self):
        if session.user is None:
            raise Forbidden

    def _check_access(self):
        self._require_user()
        if not self.event.can_manage(session.user, role=self.ROLE):
            raise Forbidden(_('You are not authorized to manage this event.'))
        check_event_locked(self, self.event)


class RHManageEventBase(RHEventBase, ManageEventMixin):
    """Base class for event management RHs"""

    DENY_FRAMES = True

    def _check_access(self):
        ManageEventMixin._check_access(self)


class RHContributionPersonListMixin:
    """List of persons somehow related to contributions (co-authors, speakers...)"""

    @property
    def _membership_filter(self):
        raise NotImplementedError

    def _process(self):
        contribution_persons = (ContributionPersonLink
                                .find(ContributionPersonLink.contribution.has(self._membership_filter))
                                .all())
        contribution_persons.extend(SubContributionPersonLink
                                    .find(SubContributionPersonLink.subcontribution
                                          .has(SubContribution.contribution.has(self._membership_filter)))
                                    .all())

        contribution_persons_dict = defaultdict(lambda: {'speaker': False, 'primary_author': False,
                                                         'secondary_author': False})
        for contrib_person in contribution_persons:
            person_roles = contribution_persons_dict[contrib_person.person]
            person_roles['speaker'] |= contrib_person.is_speaker
            person_roles['primary_author'] |= contrib_person.author_type == AuthorType.primary
            person_roles['secondary_author'] |= contrib_person.author_type == AuthorType.secondary
        return jsonify_template(self.template, event_persons=contribution_persons_dict, event=self.event)
