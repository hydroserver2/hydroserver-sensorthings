from pydantic import HttpUrl, parse_obj_as


def metadata_validator(value, values):
    """
    Validation for sensor metadata field.

    Runs a check on the sensor metadata field comparing it to the encoding_type field if present. This check ensures
    that the metadata value is consistent with the encoding type.

    :param value: The metadata value passed to the request.
    :param values: The set of values included in the body of the request.
    :return: The output value.
    """

    if values.get('encoding_type') == 'application/pdf':
        try:
            if not parse_obj_as(HttpUrl, value).lower().endswith('pdf'):
                raise AssertionError
        except AssertionError:
            raise ValueError('value is not a valid PDF link')

    elif values.get('encoding_type') == 'http://www.opengis.net/doc/IS/SensorML/2.0':
        try:
            if not parse_obj_as(HttpUrl, value).lower().endswith('xml'):
                raise AssertionError
        except AssertionError:
            raise ValueError('value is not a valid SensorML link')

    elif values.get('encoding_type') == 'text/html':
        try:
            if not parse_obj_as(HttpUrl, value).lower().endswith('html'):
                raise AssertionError
        except AssertionError:
            raise ValueError('value is not a valid HTML link')

    return value
