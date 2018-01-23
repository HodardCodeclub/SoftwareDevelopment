

from fossir.legacy.services.implementation.base import ServiceBase
from fossir.modules.rb.models.holidays import Holiday
from fossir.util.date_time import format_date, get_datetime_from_request, is_weekend
from fossir.util.i18n import _


class GetDateWarning(ServiceBase):
    UNICODE_PARAMS = True

    def _process_args(self):
        self._start_dt = get_datetime_from_request(prefix='start_', source=self._params)
        self._end_dt = get_datetime_from_request(prefix='end_', source=self._params)

    def _getAnswer(self):
        if not self._start_dt or not self._end_dt:
            return None
        start_date = self._start_dt.date()
        end_date = self._end_dt.date()
        holidays = Holiday.find_all(Holiday.date.in_([start_date, end_date]))
        if holidays:
            return _(u'Holidays chosen: {0}'.format(', '.join(h.name or format_date(h.date) for h in holidays)))
        if is_weekend(start_date) or is_weekend(end_date):
            return _(u'Weekend chosen')
        return None
