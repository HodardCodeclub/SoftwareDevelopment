

from __future__ import unicode_literals

from datetime import time

from flask import request, session
from wtforms.fields import BooleanField, HiddenField, RadioField, StringField, TextAreaField
from wtforms.validators import DataRequired, Optional

from fossir.modules.events.fields import ReviewQuestionsField
from fossir.modules.events.papers.fields import PaperEmailSettingsField
from fossir.modules.events.papers.models.review_questions import PaperReviewQuestion
from fossir.modules.events.papers.models.reviews import (PaperAction, PaperCommentVisibility, PaperReviewType,
                                                         PaperTypeProxy)
from fossir.modules.events.papers.models.revisions import PaperRevisionState
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import FormDefaults, fossirForm
from fossir.web.forms.fields import (EditableFileField, FileField, HiddenEnumField, HiddenFieldList,
                                     fossirDateTimeField, fossirEnumSelectField, fossirMarkdownField,
                                     fossirTagListField, PrincipalListField)
from fossir.web.forms.util import inject_validators
from fossir.web.forms.validators import HiddenUnless, LinkedDateTime
from fossir.web.forms.widgets import JinjaWidget, SwitchWidget


def make_review_form(event, review_type):
    """Extends the paper WTForm to add the extra fields.

    Each extra field will use a field named ``custom_ID``.

    :param event: The `Event` for which to create the paper review form.
    :param review_type: The `PaperReviewType` for which to create the paper review form.
    :return: A `PaperReviewForm` subclass.
    """
    form_class = type(b'_PaperReviewForm', (PaperReviewForm,), {})
    for idx, question in enumerate(event.cfp.get_questions_for_review_type(review_type), start=1):
        name = 'question_{}'.format(question.id)
        range_ = event.cfp.rating_range
        field = RadioField(question.text, validators=[DataRequired()],
                           choices=[(unicode(n), unicode(n)) for n in range(range_[0], range_[1] + 1)],
                           widget=JinjaWidget('events/reviews/rating_widget.html',
                                              question=question, rating_range=event.cfp.rating_range, inline_js=True,
                                              question_idx=idx))
        setattr(form_class, name, field)
    return form_class


def build_review_form(paper_revision=None, review_type=None, review=None):
    if review:
        paper_revision = review.revision
        review_type = PaperTypeProxy(review.type)
    review_form_class = make_review_form(paper_revision.paper.event, review_type=review_type.instance)
    reviews = paper_revision.get_reviews(user=session.user, group=review_type.instance)
    latest_user_review = reviews[0] if reviews else None
    if latest_user_review:
        answers = {'question_{}'.format(rating.question.id): rating.value
                   for rating in latest_user_review.ratings}
        defaults = FormDefaults(obj=latest_user_review, **answers)
    else:
        defaults = FormDefaults()

    return review_form_class(prefix='type-{}'.format(review_type.instance.value), obj=defaults,
                             paper=paper_revision.paper, edit=review is not None)


def make_competences_form(event):
    form_class = type(b'PaperCompetencesForm', (fossirForm,), {})
    for entry in event.cfp.assignees:
        name = 'competences_{}'.format(entry.id)
        field = fossirTagListField('Competences')
        setattr(form_class, name, field)
    return form_class


class PaperTeamsForm(fossirForm):
    managers = PrincipalListField(_('Paper managers'), groups=True,
                                  description=_('List of users allowed to manage the call for papers'))
    judges = PrincipalListField(_('Judges'),
                                description=_('List of users allowed to judge papers'))
    content_reviewers = PrincipalListField(_('Content reviewers'),
                                           description=_('List of users allowed to review the content of the assigned '
                                                         'papers'))
    layout_reviewers = PrincipalListField(_('Layout reviewers'),
                                          description=_('List of users allowed to review the layout of the assigned '
                                                        'papers'))

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(PaperTeamsForm, self).__init__(*args, **kwargs)
        if not self.event.cfp.content_reviewing_enabled:
            del self.content_reviewers
        if not self.event.cfp.layout_reviewing_enabled:
            del self.layout_reviewers


class PapersScheduleForm(fossirForm):
    start_dt = fossirDateTimeField(_("Start"), [Optional()], default_time=time(0, 0),
                                   description=_("The moment users can start submitting papers"))
    end_dt = fossirDateTimeField(_("End"), [Optional(), LinkedDateTime('start_dt')], default_time=time(23, 59),
                                 description=_("The moment the submission process ends"))

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(PapersScheduleForm, self).__init__(*args, **kwargs)


class PaperJudgmentFormBase(fossirForm):
    judgment_comment = TextAreaField(_("Comment"), render_kw={'placeholder': _("Leave a comment for the submitter...")})


class PaperJudgmentForm(PaperJudgmentFormBase):
    """Form for judging a single paper"""

    _order = ('judgment', 'judgment_comment')

    judgment = fossirEnumSelectField(_("Judgment"), [DataRequired()], enum=PaperAction)

    def __init__(self, *args, **kwargs):
        self.paper = kwargs.pop('paper')
        super(PaperJudgmentForm, self).__init__(*args, **kwargs)
        if self.paper.state == PaperRevisionState.to_be_corrected:
            self.judgment.skip.add(PaperAction.to_be_corrected)


class BulkPaperJudgmentForm(PaperJudgmentFormBase):
    judgment = HiddenEnumField(enum=PaperAction)
    contribution_id = HiddenFieldList()
    submitted = HiddenField()

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(BulkPaperJudgmentForm, self).__init__(*args, **kwargs)

    def is_submitted(self):
        return super(BulkPaperJudgmentForm, self).is_submitted() and 'submitted' in request.form


class PaperReviewingSettingsForm(fossirForm):
    content_review_questions = ReviewQuestionsField(
        _("Content review questions"),
        question_model=lambda: PaperReviewQuestion(type=PaperReviewType.content)
    )
    layout_review_questions = ReviewQuestionsField(
        _("Layout review questions"),
        question_model=lambda: PaperReviewQuestion(type=PaperReviewType.layout)
    )
    announcement = fossirMarkdownField(_('Announcement'), editor=True)
    email_settings = PaperEmailSettingsField(_("Email notifications"))

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(PaperReviewingSettingsForm, self).__init__(*args, **kwargs)
        if not self.event.cfp.content_reviewing_enabled:
            del self.content_review_questions
        if not self.event.cfp.layout_reviewing_enabled:
            del self.layout_review_questions


class PaperSubmissionForm(fossirForm):
    files = FileField(_("Files"), [DataRequired()], multiple_files=True)


def _get_template_data(tpl):
    return {
        'filename': tpl.filename,
        'size': tpl.size,
        'content_type': tpl.content_type,
        'url': url_for('.download_template', tpl)
    }


class PaperTemplateForm(fossirForm):
    name = StringField(_("Name"), [DataRequired()])
    description = TextAreaField(_("Description"))
    template = EditableFileField(_("Template"), add_remove_links=False, added_only=True,
                                 get_metadata=_get_template_data)

    def __init__(self, *args, **kwargs):
        template = kwargs.pop('template', None)
        if template is None:
            inject_validators(self, 'template', [DataRequired()])
        super(PaperTemplateForm, self).__init__(*args, **kwargs)


class PaperCommentForm(fossirForm):
    text = TextAreaField(_("Comment"), [DataRequired()], render_kw={'placeholder': _("Leave a comment...")})
    visibility = fossirEnumSelectField(_("Visibility"), [DataRequired()], enum=PaperCommentVisibility,
                                       skip={PaperCommentVisibility.users})

    def __init__(self, *args, **kwargs):
        comment = kwargs.get('obj')
        user = comment.user if comment else kwargs.pop('user')
        paper = kwargs.pop('paper')
        super(fossirForm, self).__init__(*args, **kwargs)
        if not paper.can_judge(user):
            self.visibility.skip.add(PaperCommentVisibility.judges)
        if not paper.can_review(user):
            del self.visibility


class PaperReviewForm(fossirForm):
    """Form for reviewing a paper"""

    _order = ('proposed_action', 'comment')

    comment = TextAreaField(_("Comment"), render_kw={'placeholder': _("You may leave a comment (only visible to "
                                                                      "reviewers and judges)...")})
    proposed_action = fossirEnumSelectField(_("Proposed Action"), [DataRequired()], enum=PaperAction)

    def __init__(self, edit=False, *args, **kwargs):
        paper = kwargs.pop('paper')
        super(PaperReviewForm, self).__init__(*args, **kwargs)
        self.event = paper.event
        if not edit:
            self.proposed_action.none = _("Propose an action...")

    @property
    def split_data(self):
        data = self.data
        return {'questions_data': {k: v for k, v in data.iteritems() if k.startswith('question_')},
                'review_data': {k: v for k, v in data.iteritems() if not k.startswith('question_')}}


class DeadlineForm(fossirForm):
    deadline = fossirDateTimeField(_("Deadline"), [Optional()], default_time=time(23, 59))
    enforce = BooleanField(_("Enforce deadline"), [HiddenUnless('deadline')], widget=SwitchWidget())

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(DeadlineForm, self).__init__(*args, **kwargs)
