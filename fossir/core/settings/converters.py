

from __future__ import unicode_literals

from datetime import timedelta

import dateutil.parser
import pytz


class SettingConverter(object):
    """
    Implement a custom conversion between Python types and
    JSON-serializable types.

    The methods are never called with a ``None`` value.
    """

    @staticmethod
    def from_python(value):
        raise NotImplementedError

    @staticmethod
    def to_python(value):
        raise NotImplementedError


class DatetimeConverter(SettingConverter):
    """Convert a tz-aware datetime object from/to an ISO-8601 string.

    The datetime is always stored as UTC, but any ISO-8601 string can
    be converted back to a datetime object as long as it has timezone
    information attached.
    """

    @staticmethod
    def from_python(value):
        assert value.tzinfo is not None
        return value.astimezone(pytz.utc).isoformat()

    @staticmethod
    def to_python(value):
        return dateutil.parser.parse(value).astimezone(pytz.utc)


class TimedeltaConverter(SettingConverter):
    """Convert a tz-aware datetime object from/to an ISO-8601 string.

    The datetime is always stored as UTC, but any ISO-8601 string can
    be converted back to a datetime object as long as it has timezone
    information attached.
    """

    @staticmethod
    def from_python(value):
        return int(value.total_seconds())

    @staticmethod
    def to_python(value):
        return timedelta(seconds=value)


class EnumConverter(SettingConverter):
    """Convert an enum object from/to its name."""

    def __init__(self, enum):
        self.enum = enum

    def from_python(self, value):
        assert isinstance(value, self.enum)
        return value.name

    def to_python(self, value):
        return self.enum[value]
