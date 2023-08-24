import pytest
from pydantic import BaseModel
from sensorthings.extras.iso_types import ISOInterval


@pytest.fixture
def interval_model():

    class IntervalModel(BaseModel):
        iso_interval: ISOInterval

    return IntervalModel


@pytest.mark.parametrize('iso_interval_value, iso_parsed_value', [
    ['2023-01-01T11:11:11+00:00/2023-01-02T11:11:11+00:00', '2023-01-01T11:11:11.000Z/2023-01-02T11:11:11.000Z'],
    ['2023-01-01T11:11:11/2023-01-02T11:11:11', '2023-01-01T11:11:11.000Z/2023-01-02T11:11:11.000Z']
])
def test_iso_interval_valid_value(interval_model, iso_interval_value, iso_parsed_value):
    interval_instance = interval_model(iso_interval=iso_interval_value)
    assert interval_instance.iso_interval == iso_parsed_value


@pytest.mark.parametrize('iso_interval_value', [
    '2023-01-01T11:11:11+00:00', '2023-01-01T11:11:11+00:00/2023-01-02T11:11:11+00:00/2023-01-03T11:11:11+00:00',
    '2023-01-02T11:11:11+00:00/2023-01-01T11:11:11+00:00', 'Jan 1, 2023/Jan 2, 2023', 123, None,
    '2023-01-01T11:11:11+00:00/2023-13-02T11:11:11+00:00', '2023-01-32T11:11:11+00:00/2023-02-02T11:11:11+00:00',
    '2023-01-01T11:11:11+00:00|2023-01-02T11:11:11+00:00'
])
def test_iso_interval_invalid_value(interval_model, iso_interval_value):
    with pytest.raises(ValueError):
        interval_model(iso_interval=iso_interval_value)
