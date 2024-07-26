import pytz
from typing import Annotated
from dateutil.parser import isoparse
from pydantic import AfterValidator, WithJsonSchema


def validate_iso_time(value: str) -> str:
    """
    Validate and format a string as an ISO time.

    Parameters
    ----------
    value : str
        The string to validate and format.

    Returns
    -------
    str
        The validated and formatted ISO time string.

    Raises
    ------
    TypeError
        If the input is not a string.
    ValueError
        If the input string is not in a valid ISO time format.
    """

    if not isinstance(value, str):
        raise TypeError('string required')
    try:
        parsed_value = isoparse(value)
        if parsed_value.tzinfo is None:
            parsed_value = parsed_value.replace(tzinfo=pytz.UTC)
        else:
            parsed_value = parsed_value.astimezone(pytz.UTC)
    except TypeError:
        raise ValueError('invalid ISO time format')

    return parsed_value.isoformat(sep='T', timespec='seconds').replace('+00:00', 'Z')


ISOTimeString = Annotated[
    str,
    AfterValidator(validate_iso_time),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


def validate_iso_interval(value: str) -> str:
    """
    Validate and format a string as an ISO interval.

    Parameters
    ----------
    value : str
        The string to validate and format.

    Returns
    -------
    str
        The validated and formatted ISO interval string.

    Raises
    ------
    TypeError
        If the input is not a string.
    ValueError
        If the input string is not in a valid ISO interval format.
    """

    if not isinstance(value, str):
        raise TypeError('string required')

    split_value = [
        validate_iso_time(dt_value) for dt_value in value.split('/')
    ]

    try:
        if len(split_value) != 2 or isoparse(split_value[0]) >= isoparse(split_value[1]):
            raise TypeError
    except TypeError:
        raise ValueError('invalid ISO interval format')

    return '/'.join(split_value)


ISOIntervalString = Annotated[
    str,
    AfterValidator(validate_iso_interval),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]
