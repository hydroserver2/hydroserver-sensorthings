import pytz
from dateutil.parser import isoparse


class ISOTime(str):

    def __datetime__(self):
        return isoparse(self)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        try:
            value = isoparse(v)
            if value.tzinfo is None:
                value = value.replace(tzinfo=pytz.UTC)
            else:
                value = value.astimezone(pytz.UTC)
        except TypeError:
            raise ValueError('invalid ISO time format')

        return cls(value.isoformat(sep='T', timespec='milliseconds').replace('+00:00', 'Z'))


class ISOInterval(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        split_v = [
            ISOTime.validate(dt_value) for dt_value in v.split('/')
        ]

        try:
            if len(split_v) != 2 or isoparse(split_v[0]) >= isoparse(split_v[1]):
                raise TypeError
        except TypeError:
            raise ValueError('invalid ISO interval format')

        return cls('/'.join(split_v))
