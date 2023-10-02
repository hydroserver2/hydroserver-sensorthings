import pytest
from pydantic import BaseModel, ValidationError
from sensorthings.validators import allow_partial


@pytest.fixture
def thing_model():

    @allow_partial
    class Thing(BaseModel):
        id: int
        name: str
        description: str = None

    return Thing


@pytest.mark.parametrize('data_values', [
    ({}),
    ({'id': 1}),
    ({'name': 'test'}),
    ({'id': 1, 'name': 'test'}),
    ({'name': 'test', 'description': 'This is a test thing.'})
])
def test_optional_fields(thing_model, data_values):
    thing = thing_model(**data_values)
    assert thing.dict(exclude_unset=True) == data_values


@pytest.mark.parametrize('data_values', [
    ({'id': None}),
    ({'id': 1, 'name': None})
])
def test_exception_on_null(thing_model, data_values):
    with pytest.raises(ValidationError):
        thing_model(**data_values)
