from django.conf import settings

ST_VERSION = '1.1'

ST_CONFORMANCE = getattr(settings, 'ST_CONFORMANCE', [
    'http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/resource-path/resource-path-to-entities',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/request-data',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/link-to-existing-entities',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/deep-insert',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/deep-insert-status-code',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity',
    'http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/historical-location-auto-creation'
])

ST_CAPABILITIES = getattr(settings, 'ST_CAPABILITIES', [
    {
        'NAME': 'Things',
        'SINGULAR_NAME': 'Thing',
        'VIEW': 'list_thing'
    },
    {
        'NAME': 'Locations',
        'SINGULAR_NAME': 'Location',
        'VIEW': 'list_location'
    },
    {
        'NAME': 'HistoricalLocations',
        'SINGULAR_NAME': 'HistoricalLocation',
        'VIEW': 'list_historical_location'
    },
    {
        'NAME': 'Datastreams',
        'SINGULAR_NAME': 'Datastream',
        'VIEW': 'list_datastream'
    },
    {
        'NAME': 'Sensors',
        'SINGULAR_NAME': 'Sensor',
        'VIEW': 'list_sensor'
    },
    {
        'NAME': 'Observations',
        'SINGULAR_NAME': 'Observation',
        'VIEW': 'list_observation'
    },
    {
        'NAME': 'ObservedProperties',
        'SINGULAR_NAME': 'ObservedProperty',
        'VIEW': 'list_observed_property'
    },
    {
        'NAME': 'FeaturesOfInterest',
        'SINGULAR_NAME': 'FeatureOfInterest',
        'VIEW': 'list_feature_of_interest'
    },
])
