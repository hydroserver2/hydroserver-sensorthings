import functools
from ninja import NinjaAPI, Schema, Router
from copy import deepcopy
from django.urls import re_path
from pydantic import BaseModel
from typing import Union, Literal, Type, NewType, List, Sequence, Optional, Callable
from hydrothings.backends.sensorthings.engine import SensorThingsEngine
from hydrothings.backends.odm2.engine import SensorThingsEngineODM2
from hydrothings.backends.frostserver.engine import FrostServerEngine
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
from hydrothings.utils import generate_response_codes


class SensorThingsAPI(NinjaAPI):
    """
    The main SensorThings API class.

    Extends the NinjaAPI class to automatically build the core SensorThings API, hook up to a backend
    datastore, and modify certain components of the SensorThings API as needed.
    """

    def __init__(
            self,
            backend: Literal['sensorthings', 'odm2', 'frostserver', None] = None,
            engine: Union[Type[NewType('SensorThingsEngine', SensorThingsAbstractEngine)], None] = None,
            components: Union[List['SensorThingsComponent'], None] = None,
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

        if not backend and not isinstance(engine, type(SensorThingsAbstractEngine)):
            raise ValueError('No backend was specified, and no engine class was defined.')

        super().__init__(**kwargs)

        self.components = components if components is not None else []
        self.endpoints = endpoints if endpoints is not None else []
        self.id_qualifier = id_qualifier

        if backend == 'sensorthings':
            self.engine = SensorThingsEngine
        elif backend == 'odm2':
            self.engine = SensorThingsEngineODM2
        elif backend == 'frostserver':
            self.engine = FrostServerEngine
        else:
            self.engine = engine

        self.add_router('', deepcopy(root_router))
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

    @staticmethod
    def _apply_authorization(view_func, auth_callbacks):
        @functools.wraps(view_func)
        def auth_wrapper(*args, **kwargs):
            for auth_callback in auth_callbacks:
                if auth_callback(*args, **kwargs) is not True:
                    return 403, {'detail': 'Forbidden'}
            return view_func(*args, **kwargs)
        return auth_wrapper

    def _build_sensorthings_router(self, component, router):

        component_settings = next(iter([
            c for c in self.components if c.name == component
        ]), None)

        endpoint_settings = {
            endpoint.name.split('_')[0]: endpoint
            for endpoint in self.endpoints
            if '_'.join(endpoint.name.split('_')[1:]) == component
        } if self.endpoints else {}

        st_router = Router(tags=router.tags)

        for path, path_operation in router.path_operations.items():
            for operation in path_operation.operations:
                view_func = deepcopy(operation.view_func)
                response_schema = getattr(operation.response_models.get(200), '__annotations__', {}).get('response')
                operation_method = operation.view_func.__name__.split('_')[0]

                if getattr(component_settings, 'component_schema', None) is not None:
                    if view_func.__annotations__.get(component):
                        for field, schema in component_settings.component_schema.__fields__.items():
                            view_func.__annotations__[component].__fields__[field] = schema

                    if response_schema:
                        if operation_method == 'list':
                            for field, schema in component_settings.component_schema.__fields__.items():
                                response_schema.__fields__['value'].type_.__fields__[field] = schema

                        elif operation_method == 'get':
                            for field, schema in component_settings.component_schema.__fields__.items():
                                response_schema.__fields__[field] = schema

                authorization_callbacks = getattr(endpoint_settings.get(operation_method), 'authorization', [])

                if isinstance(authorization_callbacks, Callable):
                    authorization_callbacks = [authorization_callbacks]
                else:
                    authorization_callbacks = []

                (getattr(st_router, operation.methods[0].lower())(
                    path.replace('(', f'({self.id_qualifier}').replace(')', f'{self.id_qualifier})'),
                    response=generate_response_codes(operation_method, response_schema),
                    deprecated=getattr(endpoint_settings.get(operation_method), 'deprecated', False),
                    by_alias=True,
                    **{
                        'auth': endpoint_settings[operation_method].authentication
                        for _ in range(1) if getattr(endpoint_settings.get(operation_method), 'authentication', None)
                    }
                ))(self._apply_authorization(view_func, authorization_callbacks))

        return st_router


class SensorThingsEndpoint(BaseModel):
    """
    The SensorThings endpoint settings class.

    This class should be used to apply endpoint level settings to a SensorThings API given the name of the endpoint.
    """

    name: str
    deprecated: bool = False
    authentication: Optional[Union[Sequence[Callable], Callable]] = None
    authorization: Optional[Union[Sequence[Callable], Callable]] = None


class SensorThingsComponent(BaseModel):
    """
    The SensorThings component settings class.

    This class should be used to apply component level settings to a SensorThings API given the name of the component.
    """

    name: str
    component_schema: Union[Type[Schema], None] = None
