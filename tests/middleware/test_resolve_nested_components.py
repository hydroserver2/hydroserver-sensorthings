from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.exceptions import Http404
from django.conf import settings
from sensorthings.middleware import SensorThingsMiddleware


class ResolveNestedComponentsTest(TestCase):
    def setUp(self):
        """
        Sets up the middleware method, request factory, and base URL used in the tests.
        """

        self.middleware = SensorThingsMiddleware(lambda request: None)
        self.factory = RequestFactory()
        self.base_url = settings.ST_BASE_URL

    def test_resolve_simple_url(self):
        """
        Sends a GET request to a standard SensorThings endpoint. The URL should resolve, and the request should have an
        associated component attribute added to it.
        """

        request_url = f'{self.base_url}/Things'
        request = self.factory.get(request_url)
        self.middleware.process_request(request)
        self.assertEqual(request.component, 'Thing')

    def test_resolve_nested_url_collection(self):
        """
        Sends a GET request to a nested SensorThings endpoint. The URL should resolve, and the request should have a
        component attribute representing the last part of the nested URL.
        """

        request_url = f'{self.base_url}/Things(1)/Datastreams'
        request = self.factory.get(request_url)
        self.middleware.process_request(request)
        self.assertEqual(request.component, 'Datastream')

    def test_resolve_nested_url_implicit_relation(self):
        """
        Sends a GET request to a nested SensorThings endpoint which includes an implicit link to a related component.
        The URL should resolve, and the request should have a component attribute representing the last part of the
        nested URL.
        """

        request_url = f'{self.base_url}/Datastreams(1)/Sensor'
        request = self.factory.get(request_url)
        self.middleware.process_request(request)
        self.assertEqual(request.component, 'Sensor')

    def test_resolve_url_address_to_property(self):
        """
        Sends a GET request to a SensorThings endpoint with an address to a valid property of the component included.
        The URL should resolve, and the request should have an associated component attribute added to it.
        """

        request_url = f'{self.base_url}/Things(1)/name'
        request = self.factory.get(request_url)
        self.middleware.process_request(request)
        self.assertEqual(request.component, 'Thing')

    def test_resolve_url_address_to_property_value(self):
        """
        Sends a GET request to a SensorThings endpoint with an address to a valid property value of the component
        included. The URL should resolve, and the request should have an associated component attribute added to it.
        """

        request_url = f'{self.base_url}/Things(1)/name/$value'
        request = self.factory.get(request_url)
        self.middleware.process_request(request)
        self.assertEqual(request.component, 'Thing')

    def test_resolve_url_address_to_property_ref(self):
        """
        Sends a GET request to a SensorThings endpoint with an address to a valid property reference of the component
        included. The URL should resolve, and the request should have an associated component attribute added to it.
        """

        request_url = f'{self.base_url}/Things(1)/name/$ref'
        request = self.factory.get(request_url)
        self.middleware.process_request(request)
        self.assertEqual(request.component, 'Thing')

    def test_resolve_url_nested_path_unrelated(self):
        """
        Sends a GET request to a nested SensorThings endpoint with an unrelated child component included in the path.
        The URL should fail to resolve and raise a Http404 exception.
        """

        request_url = f'{self.base_url}/Things(1)/Observations'
        request = self.factory.get(request_url)
        self.assertRaises(Http404, self.middleware.process_request, request)

    def test_resolve_url_address_to_property_incorrect(self):
        """
        Sends a GET request to a SensorThings endpoint addressing a property that the component doesn't have. The URL
        should fail to resolve and raise a Http404 exception.
        """

        request_url = f'{self.base_url}/Things(1)/color'
        request = self.factory.get(request_url)
        self.assertRaises(Http404, self.middleware.process_request, request)
