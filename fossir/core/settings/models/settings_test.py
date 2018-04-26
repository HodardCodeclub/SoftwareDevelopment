

from enum import Enum

import pytest

from fossir.core.settings.models.settings import Setting


@pytest.mark.usefixtures('db')
def test_set_enum():
    class Useless(int, Enum):
        thing = 1337

    Setting.set_multi('foo', {'foo': Useless.thing})
    Setting.set('foo', 'bar', Useless.thing)
    for key in {'foo', 'bar'}:
        value = Setting.get('foo', key)
        assert value == Useless.thing
        assert value == Useless.thing.value
        assert not isinstance(value, Useless)  # we store it as a plain value!
