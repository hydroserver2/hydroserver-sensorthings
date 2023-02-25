import json
from django.test import TestCase, Client
from django.conf import settings


# class CreateObservedPropertyTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.thing_data = {
#             'name': 'test',
#             'definition': 'http://www.example.com',
#             'description': 'test'
#         }
#         self.request_url = f'{settings.ST_BASE_URL}/ObservedProperties'
#
#     def test_create_observed_property(self):
#         """
#         Sends a POST request with a valid observed property body and tests that the response conforms to the
#         SensorThings specification by returning a 201 status code and a location value in the response headers.
#         """
#
#         response = self.client.post(
#             self.request_url,
#             json.dumps(self.thing_data),
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.headers.get('location'), f'http://testserver{settings.ST_BASE_URL}/ObservedProperties(1)')
