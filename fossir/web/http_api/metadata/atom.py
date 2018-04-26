

from datetime import datetime

import dateutil.parser
from pyatom import AtomFeed
from pytz import timezone, utc

from fossir.util.string import to_unicode
from fossir.web.http_api.metadata.serializer import Serializer


def _deserialize_date(date_dict):
    if isinstance(date_dict, datetime):
        return date_dict
    dt = datetime.combine(dateutil.parser.parse(date_dict['date']).date(),
                          dateutil.parser.parse(date_dict['time']).time())
    return timezone(date_dict['tz']).localize(dt).astimezone(utc)


class AtomSerializer(Serializer):

    schemaless = False
    _mime = 'application/atom+xml'

    def _execute(self, fossils):
        results = fossils['results']
        if type(results) != list:
            results = [results]

        feed = AtomFeed(
            title='fossir Feed',
            feed_url=fossils['url']
        )

        for fossil in results:
            feed.add(
                title=to_unicode(fossil['title']) or None,
                summary=to_unicode(fossil['description']) or None,
                url=fossil['url'],
                updated=_deserialize_date(fossil['startDate'])  # ugh, but that's better than creationDate
            )
        return feed.to_string()
