from django.test import TestCase
from pydantic import BaseModel, ValidationError
from sensorthings.core.utils import allow_partial


class AllowPartialDecoratorTest(TestCase):

    def setUp(self):
        """
        Defines a simple class with some required fields to test the allow_partial class decorator on.
        """

        class Thing(BaseModel):
            id: int
            name: str
            description: str = None

        self.Thing = Thing

    def test_all_optional(self):
        """
        Initializes the test class with the allow_partial decorator and passing no required values. If allow_partial
        is working correctly, the class should initialize with no field values and without raising a ValidationError.
        """

        @allow_partial
        class OptionalThing(self.Thing):
            pass

        thing = OptionalThing()

        self.assertEqual(thing.dict(exclude_unset=True), {})

    def test_some_optional(self):
        """
        Initializes the test class with an allow_partial decorator specifying the 'name' field and passing a value for
        'id'. If allow_partial is working correctly, the class should initialize with only a value for 'id' and
        without raising a ValidationError.
        """

        @allow_partial('name')
        class OptionalThing(self.Thing):
            pass

        thing = OptionalThing(id=1)

        self.assertEqual(thing.dict(exclude_unset=True), {'id': 1})

    def test_validate_none(self):
        """
        Initializes the test class with an allow_partial decorator explicitly passing a value of None to the 'id' field.
        If allow_partial is working correctly, the class should fail to initialize and raise a ValidationError.
        """

        @allow_partial
        class OptionalThing(self.Thing):
            pass

        self.assertRaises(ValidationError, OptionalThing, id=None)
