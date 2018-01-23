

from __future__ import unicode_literals

from fossir.core.db.sqlalchemy import PyIntEnum, db
from fossir.core.db.sqlalchemy.review_questions import ReviewQuestionMixin
from fossir.modules.events.papers.models.reviews import PaperReviewType


class PaperReviewQuestion(ReviewQuestionMixin, db.Model):
    __tablename__ = 'review_questions'
    __table_args__ = {'schema': 'event_paper_reviewing'}

    event_backref_name = 'paper_review_questions'

    type = db.Column(
        PyIntEnum(PaperReviewType),
        nullable=False
    )

    # relationship backrefs:
    # - ratings (PaperReviewRating.question)
