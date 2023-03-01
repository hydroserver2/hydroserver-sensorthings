from ninja import NinjaAPI, Schema
from copy import deepcopy
from django.urls import re_path
from pydantic import BaseModel
from typing import Union, Literal, Type, NewType, List
from hydrothings.backends.sensorthings.engine import SensorThingsEngine
from hydrothings.backends.odm2.engine import SensorThingsEngineODM2
from hydrothings.backends.frostserver.engine import FrostServerEngine
from hydrothings.backends.frostserver.renderers import FrostServerRenderer
from hydrothings.engine import SensorThingsAbstractEngine
from hydrothings.components.root.views import router as root_router
from hydrothings.components.datastreams.views import router as datastreams_router
from hydrothings.components.featuresofinterest.views import router as featuresofinterest_router
from hydrothings.components.historicallocations.views import router as historicallocations_router
from hydrothings.components.locations.views import router as locations_router
from hydrothings.components.observations.views import router as observations_router
from hydrothings.components.observedproperties.views import router as observedproperties_router
from hydrothings.components.sensors.views import router as sensors_router
from hydrothings.components.things.views import router as things_router


class SensorThingsAPI(NinjaAPI):

    def __init__(
            self,
            backend: Literal['sensorthings', 'odm2', 'frostserver', None] = None,
            engine: Union[Type[NewType('SensorThingsEngine', SensorThingsAbstractEngine)], None] = None,
            endpoints: Union[List['SensorThingsEndpoint'], None] = None,
            id_qualifier: str = '',
            **kwargs
    ):

        if not kwargs.get('version'):
            kwargs['version'] = '1.1'

        if kwargs.get('version') not in ['1.0', '1.1']:
            raise ValueError('Unsupported SensorThings version. Supported versions are: 1.0, 1.1')

        if backend not in ['sensorthings', 'odm2', 'frostserver', None]:
            raise ValueError(
                'Unsupported SensorThings backend. Supported backends are: "sensorthings", "odm2", "frostserver"'
            )

        if not backend and not isinstance(engine, SensorThingsAbstractEngine):
            raise ValueError('No backend was specified, and no engine class was defined.')

        super().__init__(**kwargs)

        self.endpoints = endpoints
        self.id_qualifier = id_qualifier

        if backend == 'sensorthings':
            self.engine = SensorThingsEngine
        elif backend == 'odm2':
            self.engine = SensorThingsEngineODM2
        elif backend == 'frostserver':
            self.engine = FrostServerEngine
            self.renderer = FrostServerRenderer
        else:
            self.engine = engine

        self.add_router('', self._build_sensorthings_router('root', root_router))
        self.add_router('', self._build_sensorthings_router('datastream', datastreams_router))
        self.add_router('', self._build_sensorthings_router('feature_of_interest', featuresofinterest_router))
        self.add_router('', self._build_sensorthings_router('historical_location', historicallocations_router))
        self.add_router('', self._build_sensorthings_router('location', locations_router))
        self.add_router('', self._build_sensorthings_router('observation', observations_router))
        self.add_router('', self._build_sensorthings_router('observed_property', observedproperties_router))
        self.add_router('', self._build_sensorthings_router('sensor', sensors_router))
        self.add_router('', self._build_sensorthings_router('thing', things_router))

    def _get_urls(self):

        urls = super()._get_urls()
        urls.append(re_path(r'^.*', lambda request: None, name='st_complex_handler'))

        return urls

    def _build_sensorthings_router(self, component, router):
        """"""

        router_copy = deepcopy(router)

        if self.id_qualifier:
            router_copy.path_operations = {
                path.replace('(', f'({self.id_qualifier}').replace(')', f'{self.id_qualifier})'): path_op
                for path, path_op in router_copy.path_operations.items()
            }
            for path, path_op in router_copy.path_operations.items():
                for op in path_op.operations:
                    op.path = op.path.replace('(', f'({self.id_qualifier}').replace(')', f'{self.id_qualifier})')

        if self.endpoints:
            router_endpoints = {
                endpoint.name.split('_')[0]: endpoint
                for endpoint in self.endpoints
                if '_'.join(endpoint.name.split('_')[1:]) == component
            }

            if getattr(router_endpoints.get('get', {}), 'response_schema', None):
                for path_op in router_copy.path_operations.values():
                    for op in path_op.operations:
                        if op.view_func.__name__ == f'get_{component}':
                            attrs = {
                                "__annotations__": {
                                    "response": Union[router_endpoints['get'].response_schema, str]
                                }
                            }
                            op.response_models[200] = type("NinjaResponseSchema", (Schema,), attrs)

        return router_copy


class SensorThingsEndpoint(BaseModel):
    name: str
    enabled: bool = True
    response_schema: Union[Type[Schema], None] = None
    body_schema: Union[Type[Schema], None] = None
