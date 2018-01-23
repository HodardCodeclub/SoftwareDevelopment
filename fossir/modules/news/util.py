

from __future__ import unicode_literals

from datetime import timedelta

from fossir.core.db import db
from fossir.modules.news import news_settings
from fossir.modules.news.models.news import NewsItem
from fossir.util.caching import memoize_redis
from fossir.util.date_time import now_utc


@memoize_redis(3600)
def get_recent_news():
    """Get a list of recent news for the home page"""
    settings = news_settings.get_all()
    if not settings['show_recent']:
        return []
    delta = timedelta(days=settings['max_age']) if settings['max_age'] else None
    return (NewsItem.query
            .filter(db.cast(NewsItem.created_dt, db.Date) > (now_utc() - delta).date() if delta else True)
            .order_by(NewsItem.created_dt.desc())
            .limit(settings['max_entries'])
            .all())
