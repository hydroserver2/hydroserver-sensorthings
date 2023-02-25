import json
from django.test import TestCase, Client
from django.conf import settings


# class CreateHistoricalLocationTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.historical_location_data = {
#             'time': '2023-01-01T11:11:11.111Z',
#             'Thing': {
#                 'name': 'test',
#                 'description': 'test'
#             },
#             'Locations': [
#                 {
#                     'name': 'test',
#                     'description': 'test',
#                     'encodingType': 'application/geo+json',
#                     'location': {}
#                 }
#             ]
#         }
#         self.request_url = f'{settings.ST_BASE_URL}/HistoricalLocations'
#
#     def test_create_historical_location(self):
#         """
#         Sends a POST request with a valid historical location body and tests that the response conforms to the
#         SensorThings specification by returning a 201 status code and a location value in the response headers.
#         """
#
#         response = self.client.post(
#             self.request_url,
#             json.dumps(self.historical_location_data),
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.headers.get('location'), f'http://testserver{settings.ST_BASE_URL}/HistoricalLocations(1)')
