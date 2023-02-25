from django.test import TestCase
from pydantic import BaseModel
from sensorthings.core.extras.iso_types import ISOTime


class ISOTimeTypeTest(TestCase):

    def setUp(self):
        """
        Sets up a TestModel class for testing ISOTime validation.
        """

        class TestModel(BaseModel):
            iso_time: ISOTime

        self.TestModel = TestModel

    def test_iso_time_value(self):
        """
        Tests the ISOTime type with a valid input value. No exceptions should be raised.
        """

        test_value = '2023-01-01T11:11:11+00:00'

        test_instance = self.TestModel(
            iso_time=test_value
        )

        self.assertEqual(
            test_instance.iso_time,
            test_value
        )

    def test_non_string_value(self):
        """
        Tests the ISOTime type with a non-string value. A ValueError should be raised.
        """

        test_value = 123

        self.assertRaises(ValueError, self.TestModel, iso_time=test_value)

    def test_non_iso_value(self):
        """
        Tests the ISOTime type with a non-ISO value. A ValueError should be raised.
        """

        test_value = 'Jan 1, 2023'

        self.assertRaises(ValueError, self.TestModel, iso_time=test_value)
