

from __future__ import unicode_literals

from operator import itemgetter

from flask import flash, redirect, session

from fossir.modules.events.abstracts import logger
from fossir.modules.events.abstracts.controllers.base import RHManageAbstractsBase
from fossir.modules.events.abstracts.forms import (AbstractReviewingRolesForm, AbstractReviewingSettingsForm,
                                                   AbstractsScheduleForm, AbstractSubmissionSettingsForm)
from fossir.modules.events.abstracts.models.abstracts import Abstract
from fossir.modules.events.abstracts.models.review_ratings import AbstractReviewRating
from fossir.modules.events.abstracts.models.reviews import AbstractReview
from fossir.modules.events.abstracts.operations import close_cfa, open_cfa, schedule_cfa
from fossir.modules.events.abstracts.settings import abstracts_reviewing_settings, abstracts_settings
from fossir.modules.events.abstracts.util import get_roles_for_event
from fossir.modules.events.abstracts.views import WPManageAbstracts
from fossir.modules.events.util import update_object_principals
from fossir.util.i18n import _
from fossir.util.string import handle_legacy_description
from fossir.web.flask.util import url_for
from fossir.web.forms.base import FormDefaults
from fossir.web.util import jsonify_data, jsonify_form


class RHAbstractsDashboard(RHManageAbstractsBase):
    """Dashboard of the abstracts module"""

    # Allow access even if the feature is disabled
    EVENT_FEATURE = None

    def _process(self):
        if not self.event.has_feature('abstracts'):
            return WPManageAbstracts.render_template('management/disabled.html', self.event)
        else:
            abstracts_count = Abstract.query.with_parent(self.event).count()
            return WPManageAbstracts.render_template('management/overview.html', self.event,
                                                     abstracts_count=abstracts_count, cfa=self.event.cfa)


class RHScheduleCFA(RHManageAbstractsBase):
    """Schedule the call for abstracts"""

    def _process(self):
        form = AbstractsScheduleForm(obj=FormDefaults(**abstracts_settings.get_all(self.event)),
                                     event=self.event)
        if form.validate_on_submit():
            rescheduled = self.event.cfa.start_dt is not None
            schedule_cfa(self.event, **form.data)
            if rescheduled:
                flash(_("Call for abstracts has been rescheduled"), 'success')
            else:
                flash(_("Call for abstracts has been scheduled"), 'success')
            return jsonify_data(flash=False)
        return jsonify_form(form)


class RHOpenCFA(RHManageAbstractsBase):
    """Open the call for abstracts"""

    def _process(self):
        open_cfa(self.event)
        flash(_("Call for abstracts is now open"), 'success')
        return redirect(url_for('.management', self.event))


class RHCloseCFA(RHManageAbstractsBase):
    """Close the call for abstracts"""

    def _process(self):
        close_cfa(self.event)
        flash(_("Call for abstracts is now closed"), 'success')
        return redirect(url_for('.management', self.event))


class RHManageAbstractSubmission(RHManageAbstractsBase):
    """Configure abstract submission"""

    def _process(self):
        settings = abstracts_settings.get_all(self.event)
        form = AbstractSubmissionSettingsForm(event=self.event,
                                              obj=FormDefaults(**settings))
        if form.validate_on_submit():
            abstracts_settings.set_multi(self.event, form.data)
            flash(_('Abstract submission settings have been saved'), 'success')
            return jsonify_data()
        elif not form.is_submitted():
            handle_legacy_description(form.announcement, settings,
                                      get_render_mode=itemgetter('announcement_render_mode'),
                                      get_value=itemgetter('announcement'))
        return jsonify_form(form)


class RHManageAbstractReviewing(RHManageAbstractsBase):
    """Configure abstract reviewing"""

    def _process(self):
        has_ratings = (AbstractReviewRating.query
                       .join(AbstractReviewRating.review)
                       .join(AbstractReview.abstract)
                       .filter(~Abstract.is_deleted, Abstract.event == self.event)
                       .has_rows())
        defaults = FormDefaults(abstract_review_questions=self.event.abstract_review_questions,
                                **abstracts_reviewing_settings.get_all(self.event))
        form = AbstractReviewingSettingsForm(event=self.event, obj=defaults, has_ratings=has_ratings)
        if form.validate_on_submit():
            data = form.data
            # XXX: we need to do this assignment for new questions,
            # but editing or deleting existing questions changes an
            # object that is already in the session so it's updated
            # in any case
            self.event.abstract_review_questions = data.pop('abstract_review_questions')
            abstracts_reviewing_settings.set_multi(self.event, data)
            flash(_('Abstract reviewing settings have been saved'), 'success')
            return jsonify_data()
        self.commit = False
        disabled_fields = form.RATING_FIELDS if has_ratings else ()
        return jsonify_form(form, disabled_fields=disabled_fields)


class RHManageReviewingRoles(RHManageAbstractsBase):
    """Configure track roles (reviewers/conveners)."""

    def _process(self):
        roles = get_roles_for_event(self.event)
        form = AbstractReviewingRolesForm(event=self.event, obj=FormDefaults(roles=roles))

        if form.validate_on_submit():
            role_data = form.roles.role_data
            self.event.global_conveners = set(role_data['global_conveners'])
            self.event.global_abstract_reviewers = set(role_data['global_reviewers'])

            for track, user_roles in role_data['track_roles'].viewitems():
                track.conveners = set(user_roles['convener'])
                track.abstract_reviewers = set(user_roles['reviewer'])

            # Update actual ACLs
            update_object_principals(self.event, role_data['all_conveners'], role='track_convener')
            update_object_principals(self.event, role_data['all_reviewers'], role='abstract_reviewer')

            flash(_("Abstract reviewing roles have been updated."), 'success')
            logger.info("Abstract reviewing roles of %s have been updated by %s", self.event, session.user)
            return jsonify_data()
        return jsonify_form(form, skip_labels=True, form_header_kwargs={'id': 'reviewing-role-form'},
                            disabled_until_change=True)
