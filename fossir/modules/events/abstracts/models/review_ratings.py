# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from fossir.core.db.sqlalchemy import db
from fossir.core.db.sqlalchemy.review_ratings import ReviewRatingMixin
from fossir.modules.events.abstracts.models.review_questions import AbstractReviewQuestion
from fossir.modules.events.abstracts.models.reviews import AbstractReview


class AbstractReviewRating(ReviewRatingMixin, db.Model):
    __tablename__ = 'abstract_review_ratings'
    __table_args__ = (db.UniqueConstraint('review_id', 'question_id'),
                      {'schema': 'event_abstracts'})

    question_class = AbstractReviewQuestion
    review_class = AbstractReview
