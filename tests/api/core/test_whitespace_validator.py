from django.test import TestCase
from pydantic import BaseModel, ValidationError, validator
from sensorthings.core.utils import whitespace_to_none


class WhitespaceValidatorTest(TestCase):

    def setUp(self):
        """
        Defines a simple class with the whitespace_to_none included.
        """

        class Thing(BaseModel):
            name: str

            _whitespace_validator = validator('name', allow_reuse=True, pre=True)(whitespace_to_none)

        self.Thing = Thing

    def test_empty_string(self):
        """
        Initializes the test class passing a value of '' to the 'name' field. If whitespace_to_none is working
        correctly, the class should fail to initialize and raise a ValidationError.
        """

        self.assertRaises(ValidationError, self.Thing, name='')

    def test_whitespace_string(self):
        """
        Initializes the test class passing a value of '  	' to the 'name' field. If whitespace_to_none is working
        correctly, the class should fail to initialize and raise a ValidationError.
        """

        self.assertRaises(ValidationError, self.Thing, name='  	')
