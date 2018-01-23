

from __future__ import unicode_literals

from fossir.core.db.sqlalchemy import db
from fossir.core.db.sqlalchemy.review_ratings import ReviewRatingMixin
from fossir.modules.events.papers.models.review_questions import PaperReviewQuestion
from fossir.modules.events.papers.models.reviews import PaperReview


class PaperReviewRating(ReviewRatingMixin, db.Model):
    __tablename__ = 'review_ratings'
    __table_args__ = (db.UniqueConstraint('review_id', 'question_id'),
                      {'schema': 'event_paper_reviewing'})

    question_class = PaperReviewQuestion
    review_class = PaperReview
