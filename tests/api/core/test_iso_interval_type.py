from django.test import TestCase
from pydantic import BaseModel
from sensorthings.core.extras.iso_types import ISOInterval


class ISOIntervalTypeTest(TestCase):

    def setUp(self):
        """
        Sets up a TestModel class for testing ISOInterval validation.
        """

        class TestModel(BaseModel):
            iso_interval: ISOInterval

        self.TestModel = TestModel

    def test_iso_interval_value(self):
        """
        Tests the ISOInterval type with a valid input value. No exceptions should be raised.
        """

        test_value = '2023-01-01T11:11:11+00:00/2023-01-02T11:11:11+00:00'

        test_instance = self.TestModel(
            iso_interval=test_value
        )

        self.assertEqual(
            test_instance.iso_interval,
            test_value
        )

    def test_iso_time_value(self):
        """
        Tests the ISOInterval type with an ISOTime value. A ValueError should be raised.
        """

        test_value = '2023-01-01T11:11:11+00:00'

        self.assertRaises(ValueError, self.TestModel, iso_interval=test_value)

    def test_iso_too_many_values(self):
        """
        Tests the ISOInterval type with too many time values. A ValueError should be raised.
        """

        test_value = '2023-01-01T11:11:11+00:00/2023-01-02T11:11:11+00:00/2023-01-03T11:11:11+00:00'

        self.assertRaises(ValueError, self.TestModel, iso_interval=test_value)

    def test_iso_wrong_order_interval(self):
        """
        Tests the ISOInterval type with time values in the wrong order. A ValueError should be raised.
        """

        test_value = '2023-01-02T11:11:11+00:00/2023-01-01T11:11:11+00:00'

        self.assertRaises(ValueError, self.TestModel, iso_interval=test_value)

    def test_non_iso_value(self):
        """
        Tests the ISOInterval type with non-ISO values. A ValueError should be raised.
        """

        test_value = 'Jan 1, 2023/Jan 2, 2023'

        self.assertRaises(ValueError, self.TestModel, iso_interval=test_value)

    def test_non_string_value(self):
        """
        Tests the ISOInterval type with non-string values. A ValueError should be raised.
        """

        test_value = 123

        self.assertRaises(ValueError, self.TestModel, iso_interval=test_value)
