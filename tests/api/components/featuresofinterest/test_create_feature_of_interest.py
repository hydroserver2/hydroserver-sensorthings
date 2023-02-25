import json
from django.test import TestCase, Client
from django.conf import settings


# class CreateLocationTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.feature_of_interest_data = {
#             'name': 'test_feature',
#             'description': 'A test feature.',
#             'encodingType': 'application/geo+json',
#             'feature': {}
#         }
#         self.request_url = f'{settings.ST_BASE_URL}/FeaturesOfInterest'
#
#     def test_create_feature_of_interest(self):
#         """
#         Sends a POST request with a valid location body and tests that the response conforms to the SensorThings
#         specification by returning a 201 status code and a location value in the response headers.
#         """
#
#         response = self.client.post(
#             self.request_url,
#             json.dumps(self.feature_of_interest_data),
#             content_type='application/json'
#         )
#
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.headers.get('location'), f'http://testserver{settings.ST_BASE_URL}/FeaturesOfInterest(1)')
