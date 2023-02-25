import json
from django.test import TestCase, Client
from django.conf import settings


# class CreateSensorTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.sensor_data = {
#             'name': 'test_sensor',
#             'description': 'A test sensor.',
#             'encodingType': 'application/pdf',
#             'metadata': 'http://www.example.com/test.pdf'
#         }
#         self.request_url = f'{settings.ST_BASE_URL}/Sensors'
#
#     def test_create_sensor(self):
#         """
#         Sends a POST request with a valid sensor body and tests that the response conforms to the SensorThings
#         specification by returning a 201 status code and a location value in the response headers.
#         """
#
#         response = self.client.post(
#             self.request_url,
#             json.dumps(self.sensor_data),
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.headers.get('location'), f'http://testserver{settings.ST_BASE_URL}/Sensors(1)')
