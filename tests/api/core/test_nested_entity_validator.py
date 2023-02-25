from django.test import TestCase


class NestedEntityValidatorTest(TestCase):

    def setUp(self):
        """
        Defines test data for creating nested instances of Things and Locations.
        """

        self.thing_data = [
            {
                'name': 'test_sensor',
                'description': 'A test sensor.'
            }
        ]

        self.location_data = [
            {
                'name': 'logan',
                'description': 'Logan, UT',
                'encodingType': 'application/geo+json',
                'location': {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [41.74, -111.83]
                    }
                }
            }
        ]
