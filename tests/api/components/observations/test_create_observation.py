import json
from django.test import TestCase, Client
from django.conf import settings


# class CreateObservationTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.observation_data = {
#             'phenomenonTime': '2023-01-01T11:11:11+00:00',
#             'resultTime': '2023-01-01T11:11:11+00:00',
#             'result': 'test',
#             'FeatureOfInterest': {
#                 'name': 'test',
#                 'description': 'test',
#                 'encodingType': 'application/geo+json',
#                 'feature': {}
#             },
#             'Datastream': {
#                 'name': 'test_datastream',
#                 'description': 'A test datastream.',
#                 'unitOfMeasurement': {
#                     'name': 'Cubic feet per second',
#                     'symbol': 'CFS',
#                     'definition': 'http://www.example.com'
#                 },
#                 'observationType': 'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation',
#                 'Thing': {
#                     'name': 'test',
#                     'description': 'test'
#                 },
#                 'Sensor': {
#                     'name': 'test',
#                     'description': 'test',
#                     'encodingType': 'application/pdf',
#                     'metadata': 'http://www.example.com/test.pdf'
#                 },
#                 'ObservedProperty': {
#                     'name': 'test',
#                     'definition': 'http://www.example.com',
#                     'description': 'test'
#                 }
#             }
#         }
#         self.request_url = f'{settings.ST_BASE_URL}/Observations'
#
#     def test_create_observation(self):
#         """
#         Sends a POST request with a valid observation body and tests that the response conforms to the SensorThings
#         specification by returning a 201 status code and a location value in the response headers.
#         """
#
#         response = self.client.post(
#             self.request_url,
#             json.dumps(self.observation_data),
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.headers.get('location'), f'http://testserver{settings.ST_BASE_URL}/Observations(1)')
