from datetime import datetime


class ISOTime(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        try:
            datetime.fromisoformat(v)
        except TypeError:
            raise ValueError('invalid ISO time format')

        return cls(v)


class ISOInterval(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        split_v = v.split('/')

        try:
            if len(split_v) != 2 or datetime.fromisoformat(split_v[0]) >= datetime.fromisoformat(split_v[1]):
                raise TypeError
        except TypeError:
            raise ValueError('invalid ISO interval format')

        return cls(v)
