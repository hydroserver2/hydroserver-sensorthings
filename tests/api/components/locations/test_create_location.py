import json
from django.test import TestCase, Client
from django.conf import settings


# class CreateLocationTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.location_data = {
#             'name': 'test_location',
#             'description': 'A test location.',
#             'encodingType': 'application/geo+json',
#             'location': {}
#         }
#         self.request_url = f'{settings.ST_BASE_URL}/Locations'
#
#     def test_create_location(self):
#         """
#         Sends a POST request with a valid location body and tests that the response conforms to the SensorThings
#         specification by returning a 201 status code and a location value in the response headers.
#         """
#
#         response = self.client.post(
#             self.request_url,
#             json.dumps(self.location_data),
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.headers.get('location'), f'http://testserver{settings.ST_BASE_URL}/Locations(1)')
