

from datetime import datetime

import pytest

from fossir.modules.rb.models.room_nonbookable_periods import NonBookablePeriod


@pytest.mark.parametrize(('start_dt', 'end_dt', 'expected'), (
    ('2017-12-04 00:00', '2017-12-06 00:00', True),
    ('2017-12-05 00:01', '2017-12-05 00:01', True),
    ('2017-12-05 00:00', '2017-12-05 00:00', False),
    ('2017-12-01 00:00', '2017-12-05 00:00', False),
    ('2017-12-06 00:00', '2017-12-07 00:00', False),
))
def test_overlaps(start_dt, end_dt, expected):
    start_dt = datetime.strptime(start_dt, '%Y-%m-%d %H:%M')
    end_dt = datetime.strptime(end_dt, '%Y-%m-%d %H:%M')
    nbp = NonBookablePeriod(start_dt=datetime(2017, 12, 5), end_dt=datetime(2017, 12, 6))
    assert nbp.overlaps(start_dt, end_dt) == expected
