import pytest
from pydantic import BaseModel, ValidationError, validator
from hydrothings.components.sensors.utils import metadata_validator


@pytest.mark.parametrize('metadata_value, encoding_value', [
    ('http://www.example.com/test.pdf', 'application/pdf'),
    ('http://www.example.com/test.xml', 'http://www.opengis.net/doc/IS/SensorML/2.0'),
    ('http://www.example.com/test.html', 'text/html'),
])
def test_valid_metadata_values(metadata_value, encoding_value):
    validated_value = metadata_validator(
        value=metadata_value,
        values={
            'encoding_type': encoding_value
        }
    )
    assert validated_value == metadata_value


@pytest.mark.parametrize('metadata_value, encoding_value', [
    ('http://www.example.com/test.xml', 'application/pdf'),
    ('http://www.example.com/test.html', 'application/pdf'),
    ('http://www.example.com/test.pdf', 'http://www.opengis.net/doc/IS/SensorML/2.0'),
    ('http://www.example.com/test.html', 'http://www.opengis.net/doc/IS/SensorML/2.0'),
    ('http://www.example.com/test.pdf', 'text/html'),
    ('http://www.example.com/test.xml', 'text/html'),
    ('not/a/valid/url.pdf', 'application/pdf'),
    ('not/a/valid/url.xml', 'http://www.opengis.net/doc/IS/SensorML/2.0'),
    ('not/a/valid/url.html', 'text/html')
])
def test_valid_metadata_values(metadata_value, encoding_value):
    with pytest.raises(ValueError):
        metadata_validator(
            value=metadata_value,
            values={
                'encoding_type': encoding_value
            }
        )
