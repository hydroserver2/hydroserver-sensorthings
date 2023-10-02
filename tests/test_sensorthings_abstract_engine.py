import pytest
from unittest.mock import patch
from sensorthings import SensorThingsAbstractEngine


@pytest.fixture
def host():
    return '127.0.0.1:8000'


@pytest.fixture
def scheme():
    return 'http'


@pytest.fixture
def version():
    return '1.1'


@pytest.mark.parametrize('path, entity_id, related_component, ref_url', [
    ('Things', None, None, f'/sensorthings/v1.1/Things'),
    ('Things', 1, None, f'/sensorthings/v1.1/Things(1)'),
    ('Things', 1, 'Locations', f'/sensorthings/v1.1/Things(1)/Locations')
])
@patch.object(SensorThingsAbstractEngine, '__init__', lambda self: None)
@patch.multiple(SensorThingsAbstractEngine, __abstractmethods__=set())
def test_engine_get_ref(scheme, host, version, path, entity_id, related_component, ref_url):
    engine = SensorThingsAbstractEngine()
    engine.scheme = scheme
    engine.host = host
    engine.path = path
    engine.version = version

    assert engine.get_ref(entity_id, related_component) == f'{scheme}://{host}{ref_url}'


@pytest.mark.parametrize('component, related_components', [
    ('Thing', {'locations': 'Locations', 'historical_locations': 'HistoricalLocations', 'datastreams': 'Datastreams'}),
    ('Datastream', {
        'thing': 'Thing', 'sensor': 'Sensor', 'observed_property': 'ObservedProperty', 'observations': 'Observations'
    }),
    ('Location', {'things': 'Things', 'historical_locations': 'HistoricalLocations'}),
    ('HistoricalLocation', {'thing': 'Thing', 'locations': 'Locations'}),
    ('Sensor', {'datastreams': 'Datastreams'}),
    ('ObservedProperty', {'datastreams': 'Datastreams'}),
    ('Observation', {'datastream': 'Datastream', 'feature_of_interest': 'FeatureOfInterest'}),
    ('FeatureOfInterest', {'observations': 'Observations'})
])
@patch.object(SensorThingsAbstractEngine, '__init__', lambda self: None)
@patch.multiple(SensorThingsAbstractEngine, __abstractmethods__=set())
def test_engine_get_related_components(component, related_components):
    engine = SensorThingsAbstractEngine()
    engine.component = component

    assert engine.get_related_components() == related_components


@pytest.mark.parametrize('path, component, entity, is_collection, related_links', [
    ('Things(1)', 'Thing', {}, False, {
        'locations_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Things(1)/Locations',
        'historical_locations_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Things(1)/HistoricalLocations',
        'datastreams_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Things(1)/Datastreams'
    }),
    ('Locations(1)', 'Location', {}, False, {
        'things_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Locations(1)/Things',
        'historical_locations_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Locations(1)/HistoricalLocations'
    }),
    ('HistoricalLocations(1)', 'HistoricalLocation', {}, False, {
        'thing_link': 'http://127.0.0.1:8000/sensorthings/v1.1/HistoricalLocations(1)/Thing',
        'locations_link': 'http://127.0.0.1:8000/sensorthings/v1.1/HistoricalLocations(1)/Locations'
    }),
    ('Sensors(1)', 'Sensor', {}, False, {
        'datastreams_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Sensors(1)/Datastreams'
    }),
    ('ObservedProperties(1)', 'ObservedProperty', {}, False, {
        'datastreams_link': 'http://127.0.0.1:8000/sensorthings/v1.1/ObservedProperties(1)/Datastreams'
    }),
    ('Datastreams(1)', 'Datastream', {}, False, {
        'thing_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Datastreams(1)/Thing',
        'sensor_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Datastreams(1)/Sensor',
        'observed_property_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Datastreams(1)/ObservedProperty',
        'observations_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Datastreams(1)/Observations',
    }),
    ('Observations(1)', 'Observation', {}, False, {
        'datastream_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Observations(1)/Datastream',
        'feature_of_interest_link': 'http://127.0.0.1:8000/sensorthings/v1.1/Observations(1)/FeatureOfInterest'
    }),
    ('FeaturesOfInterest(1)', 'FeatureOfInterest', {}, False, {
        'observations_link': 'http://127.0.0.1:8000/sensorthings/v1.1/FeaturesOfInterest(1)/Observations'
    }),
])
@patch.object(SensorThingsAbstractEngine, '__init__', lambda self: None)
@patch.multiple(SensorThingsAbstractEngine, __abstractmethods__=set())
def test_engine_build_related_links(scheme, host, version, path, component, entity, is_collection: bool, related_links):
    engine = SensorThingsAbstractEngine()
    engine.scheme = scheme
    engine.host = host
    engine.path = path
    engine.component = component
    engine.version = version

    assert engine.build_related_links(entity, is_collection) == related_links