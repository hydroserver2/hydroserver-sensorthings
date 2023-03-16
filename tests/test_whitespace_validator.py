import pytest
from pydantic import BaseModel, ValidationError, validator
from hydrothings.validators import whitespace_to_none


@pytest.fixture
def thing_model():

    class Thing(BaseModel):
        name: str
        description: str = None

        _whitespace_validator = validator('*', allow_reuse=True, pre=True)(whitespace_to_none)

    return Thing


@pytest.mark.parametrize('data_values, description_model_value', [
    ({'name': 'test', 'description': ''}, None),
    ({'name': 'test', 'description': '  '}, None),
    ({'name': 'test', 'description': '	'}, None),
    ({'name': 'test', 'description': '   Test description.	'}, 'Test description.')
])
def test_trim_whitespace(thing_model, data_values, description_model_value):
    thing = thing_model(**data_values)
    assert thing.description == description_model_value


@pytest.mark.parametrize('data_values', [
    ({'name': '', 'description': 'Test description.'}),
    ({'name': '  ', 'description': 'Test description.'}),
    ({'name': '	', 'description': 'Test description.'})
])
def test_exception_on_whitespace(thing_model, data_values):
    with pytest.raises(ValidationError):
        thing_model(**data_values)
