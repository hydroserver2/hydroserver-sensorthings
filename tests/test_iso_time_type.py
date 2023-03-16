import pytest
from pydantic import BaseModel
from hydrothings.extras.iso_types import ISOTime


@pytest.fixture
def time_model():

    class TimeModel(BaseModel):
        iso_time: ISOTime

    return TimeModel


@pytest.mark.parametrize('iso_time_value', [
    '2023-01-01T11:11:11+00:00', '2023-01-01T11:11:11'
])
def test_iso_time_valid_value(time_model, iso_time_value):
    time_instance = time_model(iso_time=iso_time_value)
    assert time_instance.iso_time == iso_time_value


@pytest.mark.parametrize('iso_time_value', [
    123, None, 'Jan 1, 2023', '2023-13-01T11:11:11'
])
def test_iso_time_invalid_value(time_model, iso_time_value):
    with pytest.raises(ValueError):
        time_model(iso_time=iso_time_value)
