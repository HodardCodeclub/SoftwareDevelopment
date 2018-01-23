

from __future__ import unicode_literals

from flask import render_template, session

from fossir.modules.events.abstracts.util import get_visible_reviewed_for_tracks
from fossir.modules.events.management.views import WPEventManagement
from fossir.modules.events.views import WPConferenceDisplayBase
from fossir.util.mathjax import MathjaxMixin


class WPManageAbstracts(MathjaxMixin, WPEventManagement):
    template_prefix = 'events/abstracts/'
    sidemenu_option = 'abstracts'

    def getJSFiles(self):
        return (WPEventManagement.getJSFiles(self) +
                self._asset_env['markdown_js'].urls() +
                self._asset_env['selectize_js'].urls() +
                self._asset_env['modules_reviews_js'].urls() +
                self._asset_env['modules_abstracts_js'].urls())

    def getCSSFiles(self):
        return WPEventManagement.getCSSFiles(self) + self._asset_env['selectize_css'].urls()

    def _getHeadContent(self):
        return WPEventManagement._getHeadContent(self) + MathjaxMixin._getHeadContent(self)


class WPDisplayAbstractsBase(WPConferenceDisplayBase):
    template_prefix = 'events/abstracts/'

    def getJSFiles(self):
        return (WPConferenceDisplayBase.getJSFiles(self) +
                self._asset_env['markdown_js'].urls() +
                self._asset_env['selectize_js'].urls() +
                self._asset_env['modules_reviews_js'].urls() +
                self._asset_env['modules_abstracts_js'].urls())

    def getCSSFiles(self):
        return WPConferenceDisplayBase.getCSSFiles(self) + self._asset_env['selectize_css'].urls()


class WPDisplayAbstracts(WPDisplayAbstractsBase):
    menu_entry_name = 'call_for_abstracts'


class WPDisplayCallForAbstracts(WPDisplayAbstracts):
    def getJSFiles(self):
        return WPDisplayAbstractsBase.getJSFiles(self) + self._asset_env['modules_event_display_js'].urls()


class WPDisplayAbstractsReviewing(WPDisplayAbstracts):
    menu_entry_name = 'abstract_reviewing_area'

    def getJSFiles(self):
        return WPDisplayAbstracts.getJSFiles(self) + self._asset_env['modules_event_management_js'].urls()


def render_abstract_page(abstract, view_class=None, management=False):
    from fossir.modules.events.abstracts.forms import (AbstractCommentForm, AbstractJudgmentForm,
                                                       AbstractReviewedForTracksForm, build_review_form)
    comment_form = AbstractCommentForm(abstract=abstract, user=session.user, formdata=None)
    review_form = None
    reviewed_for_tracks = list(abstract.get_reviewed_for_groups(session.user))
    if len(reviewed_for_tracks) == 1:
        review_form = build_review_form(abstract, reviewed_for_tracks[0])
    judgment_form = AbstractJudgmentForm(abstract=abstract, formdata=None)
    review_track_list_form = AbstractReviewedForTracksForm(event=abstract.event, obj=abstract, formdata=None)
    params = {'abstract': abstract,
              'comment_form': comment_form,
              'review_form': review_form,
              'review_track_list_form': review_track_list_form,
              'judgment_form': judgment_form,
              'visible_tracks': get_visible_reviewed_for_tracks(abstract, session.user),
              'management': management}
    if view_class:
        return view_class.render_template('abstract.html', abstract.event, **params)
    else:
        return render_template('events/abstracts/abstract.html', no_javascript=True, standalone=True, **params)
