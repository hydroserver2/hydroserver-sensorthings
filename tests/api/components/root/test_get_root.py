import json
from django.test import TestCase, Client
from django.conf import settings


# class GetRootTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.request_url = settings.ST_BASE_URL + '/'
#
#     def test_get_root(self):
#         """
#         Sends a GET request to the server root resource path and tests that the response conforms to the SensorThings
#         specification by returning a 201 status code and that the response body contains a 'serverSettings' value.
#         """
#
#         response = self.client.get(self.request_url, secure=True)
#         response_content = json.loads(response.content)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('serverSettings' in response_content)
