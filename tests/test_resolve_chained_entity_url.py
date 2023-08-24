import pytest
from django.test.client import RequestFactory
from django.urls.exceptions import Http404
from sensorthings.middleware import SensorThingsMiddleware


@pytest.fixture
def middleware():
    return SensorThingsMiddleware(lambda request: None)


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def service_base_url():
    return '/test-app/v1.1'


success_test_parameters = {
    'simple_url': [
        ['Things', 'Thing', []], ['Locations', 'Location', []], ['HistoricalLocations', 'HistoricalLocation', []],
        ['Sensors', 'Sensor', []], ['ObservedProperties', 'ObservedProperty', []], ['Datastreams', 'Datastream', []],
        ['Observations', 'Observation', []], ['FeaturesOfInterest', 'FeatureOfInterest', []]
    ],
    'chained_collection_url': [
        ['Things(1)/Datastreams', 'Datastream', [('Thing', '1')]],
        ['Things(2)/Locations', 'Location', [('Thing', '2')]],
        ['Datastreams(3)/Observations', 'Observation', [('Datastream', '3')]],
        ['Locations(4)/Things', 'Thing', [('Location', '4')]],
    ],
    'chained_implicit_url': [
        ['Datastreams(1)/Sensor', 'Sensor', [('Datastream', '1')]],
        ['Datastreams(2)/Thing', 'Thing', [('Datastream', '2')]],
        ['Datastreams(3)/ObservedProperty', 'ObservedProperty', [('Datastream', '3')]],
        ['Observations(4)/Datastream', 'Datastream', [('Observation', '4')]],
    ],
    'address_to_property_url': [
        ['Things(1)/name', 'Thing', []],
        ['Datastreams(2)/description', 'Datastream', []]
    ],
    'address_to_value_url': [
        ['Things(1)/name/$value', 'Thing', []],
        ['Datastreams(2)/description/$value', 'Datastream', []]
    ],
    'address_to_ref_url': [
        ['Things(1)/name/$ref', 'Thing', []],
        ['Datastreams(2)/description/$ref', 'Datastream', []]
    ]
}

failure_test_parameters = {
    'chained_unrelated_collection_url': [
        'Things(1)/Observations',
        'ObservedProperties(2)/Things'
    ],
    'chained_unrelated_implicit_url': [
        'Things(1)/Sensor',
        'Datastreams(2)/Observation'
    ],
    'address_to_nonexistent_property_url': [
        'Things(1)/color'
    ],
    'address_to_value_and_ref_url': [
        'Things(1)/name/$value/$ref'
    ]
}


@pytest.mark.parametrize('parameter_group, url, component, entity_chain', [
    tuple([parameter_group] + parameter) for parameter_group, parameters
    in success_test_parameters.items() for parameter in parameters
])
def test_successful_url_resolution_cases(
        parameter_group, url, component, entity_chain, service_base_url, middleware, request_factory
):
    request_url = f'{service_base_url}/{url}'
    request = request_factory.get(request_url)
    middleware.process_request(request)
    assert request.component == component
    assert request.entity_chain == entity_chain


@pytest.mark.parametrize('parameter_group, url', [
    (parameter_group, parameter,) for parameter_group, parameters
    in failure_test_parameters.items() for parameter in parameters
])
def test_failing_url_resolution_cases(
        parameter_group, url, service_base_url, middleware, request_factory
):
    request_url = f'{service_base_url}/{url}'
    request = request_factory.get(request_url)
    with pytest.raises(Http404):
        middleware.process_request(request)
