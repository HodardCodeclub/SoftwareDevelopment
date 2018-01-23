

from datetime import date, datetime, time, timedelta

import pytest

from fossir.core.errors import fossirError
from fossir.modules.rb.models.reservations import RepeatFrequency
from fossir.modules.rb.models.util import unimplemented
from fossir.testing.util import bool_matrix


pytest_plugins = 'fossir.modules.rb.testing.fixtures'


@pytest.mark.parametrize(('raised', 'caught', 'message'), (
    (RuntimeError, fossirError, 'foo'),
    (Exception,    Exception,   'bar'),
    (ValueError,   ValueError,  'bar')
))
def test_unimplemented(raised, caught, message):
    @unimplemented(RuntimeError, message='foo')
    def _func():
        raise raised('bar')

    exc_info = pytest.raises(caught, _func)
    assert exc_info.value.message == message


@pytest.mark.parametrize(
    ('not_repeating', 'only_one_valid', 'propagate', 'proxied'),
    bool_matrix('..0', expect=False) +
    bool_matrix('..1', expect='any_dynamic')
)
@pytest.mark.usefixtures('smtp')
def test_proxy_to_reservation_if_last_valid_occurrence(db, mock, create_reservation, dummy_user,
                                                       not_repeating, only_one_valid, propagate, proxied):
    resv = create_reservation(start_dt=datetime.combine(date.today(), time(8)),
                              end_dt=datetime.combine(date.today() + timedelta(days=1), time(17)),
                              repeat_frequency=RepeatFrequency.NEVER if not_repeating else RepeatFrequency.DAY)
    if only_one_valid:
        for occ in resv.occurrences[1:]:
            occ.is_cancelled = True
        db.session.flush()

    occ = resv.occurrences.first()
    mock.patch.object(resv, 'cancel')
    occ.cancel(user=dummy_user, propagate=propagate)
    assert resv.cancel.called == proxied
