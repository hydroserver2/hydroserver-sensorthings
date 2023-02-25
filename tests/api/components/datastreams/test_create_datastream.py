import json
from django.test import TestCase, Client
from django.conf import settings


# class CreateDatastreamTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.datastream_data = {
#             'name': 'test_datastream',
#             'description': 'A test datastream.',
#             'unitOfMeasurement': {
#                 'name': 'Cubic feet per second',
#                 'symbol': 'CFS',
#                 'definition': 'http://www.example.com'
#             },
#             'observationType': 'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation',
#             'Thing': {
#                 'name': 'test',
#                 'description': 'test'
#             },
#             'Sensor': {
#                 'name': 'test',
#                 'description': 'test',
#                 'encodingType': 'application/pdf',
#                 'metadata': 'http://www.example.com/test.pdf'
#             },
#             'ObservedProperty': {
#                 'name': 'test',
#                 'definition': 'http://www.example.com',
#                 'description': 'test'
#             }
#         }
#         self.request_url = f'{settings.ST_BASE_URL}/Datastreams'
#
#     def test_create_datastream(self):
#         """
#         Sends a POST request with a valid datastream body and tests that the response conforms to the SensorThings
#         specification by returning a 201 status code and a location value in the response headers.
#         """
#
#         response = self.client.post(
#             self.request_url,
#             json.dumps(self.datastream_data),
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.headers.get('location'), f'http://testserver{settings.ST_BASE_URL}/Datastreams(1)')
