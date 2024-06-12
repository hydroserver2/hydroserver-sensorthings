import functools
from ninja import NinjaAPI
from copy import deepcopy
from django.urls import re_path
from pydantic import BaseModel
from typing import Union, Type, NewType, List, Sequence, Optional, Callable
from sensorthings.engine import SensorThingsBaseEngine
from sensorthings.renderer import SensorThingsRenderer
from sensorthings.router import SensorThingsRouter
from sensorthings.components.root.views import router as root_router
from sensorthings.components.root.views import handle_advanced_path
from sensorthings.components.datastreams.views import router as datastreams_router
from sensorthings.components.featuresofinterest.views import router as featuresofinterest_router
from sensorthings.components.historicallocations.views import router as historicallocations_router
from sensorthings.components.locations.views import router as locations_router
from sensorthings.components.observations.views import router as observations_router
from sensorthings.components.observedproperties.views import router as observedproperties_router
from sensorthings.components.sensors.views import router as sensors_router
from sensorthings.components.things.views import router as things_router
from sensorthings.components import get_response_schemas
from sensorthings.extensions.dataarray.engine import DataArrayBaseEngine
from sensorthings.extensions.dataarray.views import router as data_array_router


class SensorThingsAPI(NinjaAPI):
    """
    Custom API class for SensorThings, extending NinjaAPI.

    This class initializes the API, sets up routing, and integrates
    with SensorThings components and endpoints.
    """

    def __init__(
            self,
            engine: Union[Type[NewType('SensorThingsEngine', SensorThingsBaseEngine)], None] = None,
            endpoints: Union[List['SensorThingsEndpoint'], None] = None,
            **kwargs
    ):
        """
        Initialize the SensorThingsAPI.

        Parameters
        ----------
        engine : Type, optional
            The engine class for SensorThings. Default is None.
        endpoints : List[SensorThingsEndpoint], optional
            A list of endpoints for the API. Default is None.

        Raises
        ------
        ValueError
            If an unsupported SensorThings version is provided.
        """

        if not kwargs.get('version'):
            kwargs['version'] = '1.1'

        if kwargs.get('version') not in ['1.0', '1.1']:
            raise ValueError('Unsupported SensorThings version. Supported versions are: 1.0, 1.1')

        if 'urls_namespace' not in kwargs:
            kwargs['urls_namespace'] = f'sensorthings-v{kwargs["version"]}-api'
        else:
            kwargs['urls_namespace'] += f'sensorthings-v{kwargs["version"]}-api'

        super().__init__(
            renderer=SensorThingsRenderer(),
            **kwargs
        )

        self.endpoints = endpoints if endpoints is not None else []
        self.engine = engine

        self.add_router('', deepcopy(root_router))
        self.add_router('', self._build_sensorthings_router('thing', things_router))
        self.add_router('', self._build_sensorthings_router('location', locations_router))
        self.add_router('', self._build_sensorthings_router('historical_location', historicallocations_router))
        self.add_router('', self._build_sensorthings_router('observed_property', observedproperties_router))
        self.add_router('', self._build_sensorthings_router('sensor', sensors_router))
        self.add_router('', self._build_sensorthings_router('datastream', datastreams_router))
        self.add_router('', self._build_sensorthings_router('feature_of_interest', featuresofinterest_router))

        if issubclass(self.engine, DataArrayBaseEngine):
            self.add_router('', self._build_sensorthings_router('observation', data_array_router))
        else:
            self.add_router('', self._build_sensorthings_router('observation', observations_router))

        self.get_response_schemas = {
            get_response_schema_name: next((
                endpoint.response_schema for endpoint in self.endpoints
                if hasattr(endpoint.response_schema, '__name__')
                and endpoint.response_schema.__name__ == get_response_schema_name
            ), None)
            or getattr(get_response_schemas, get_response_schema_name)
            for get_response_schema_name in dir(get_response_schemas)
            if get_response_schema_name.endswith('GetResponse')
        }

        handle_advanced_path.__api__ = self

    def _get_urls(self):
        """
        Override the method to include advanced path handling URL.

        Returns
        -------
        list
            List of URL patterns.
        """

        urls = super()._get_urls()
        urls.append(re_path(r'^.*', handle_advanced_path, name='advanced_path_handler'))

        return urls

    @staticmethod
    def _apply_authorization(view_func, auth_callbacks):
        """
        Apply authorization callbacks to the view function.

        Parameters
        ----------
        view_func : Callable
            The view function to wrap with authorization.
        auth_callbacks : list of Callable
            List of authorization callback functions.

        Returns
        -------
        Callable
            The wrapped view function with authorization checks.
        """

        @functools.wraps(view_func)
        def auth_wrapper(*args, **kwargs):
            for auth_callback in auth_callbacks:
                if auth_callback(*args, **kwargs) is not True:
                    return 403, {'detail': 'Forbidden'}
            return view_func(*args, **kwargs)
        return auth_wrapper

    def _build_sensorthings_router(self, component, router):
        """
        Build a SensorThings router for a specific component.

        Parameters
        ----------
        component : str
            The component name.
        router : Router
            The router instance for the component.

        Returns
        -------
        SensorThingsRouter
            The built router with paths and operations.
        """

        endpoint_settings = {
            endpoint.name.split('_')[0]: endpoint
            for endpoint in self.endpoints
            if '_'.join(endpoint.name.split('_')[1:]) == component
        } if self.endpoints else {}

        st_router = SensorThingsRouter(tags=router.tags)

        for path, path_operation in router.path_operations.items():
            for operation in path_operation.operations:
                view_func = deepcopy(operation.view_func)
                operation_method = operation.view_func.__name__.split('_')[0]

                response_schema = getattr(operation.response_models.get(200), '__annotations__', {}).get('response')
                custom_response_schema = getattr(endpoint_settings.get(operation_method, None), 'response_schema', None)
                if isinstance(custom_response_schema, list):
                    custom_response_schema = custom_response_schema[0]
                if custom_response_schema:
                    response_schemas = tuple([custom_response_schema, *response_schema.__args__[1:-1]])
                elif hasattr(response_schema, '__args__'):
                    response_schemas = tuple([*response_schema.__args__[:-1]])
                elif response_schema:
                    response_schemas = (response_schema,)
                else:
                    response_schemas = None

                if getattr(endpoint_settings.get(operation_method, None), 'body_schema', None) is not None:
                    view_func.__annotations__[component] = endpoint_settings[operation_method].body_schema

                authorization_callbacks = getattr(endpoint_settings.get(operation_method), 'authorization', [])

                if isinstance(authorization_callbacks, Callable):
                    authorization_callbacks = [authorization_callbacks]
                else:
                    authorization_callbacks = []

                (getattr(st_router, f'st_{operation.methods[0].lower()}')(
                    path,
                    response_schemas=response_schemas,
                    deprecated=getattr(endpoint_settings.get(operation_method), 'deprecated', False),
                    **{
                        'auth': endpoint_settings[operation_method].authentication
                        for _ in range(1) if getattr(endpoint_settings.get(operation_method), 'authentication', None)
                    }
                ))(self._apply_authorization(view_func, authorization_callbacks))

        return st_router


class SensorThingsEndpoint(BaseModel):
    """
    Data model for defining a SensorThings API endpoint.

    Attributes
    ----------
    name : str
        The name of the endpoint.
    deprecated : bool, optional
        Whether the endpoint is deprecated. Default is False.
    authentication : Optional[Union[Sequence[Callable], Callable]], optional
        Authentication callbacks. Default is None.
    authorization : Optional[Union[Sequence[Callable], Callable]], optional
        Authorization callbacks. Default is None.
    body_schema : Optional[Type], optional
        The schema for the request body. Default is None.
    response_schema : Union[List[Type], Type, None], optional
        The schema for the response. Default is None.
    """

    name: str
    deprecated: bool = False
    authentication: Optional[Union[Sequence[Callable], Callable]] = None
    authorization: Optional[Union[Sequence[Callable], Callable]] = None
    body_schema: Optional[Type] = None
    response_schema: Union[List[Type], Type, None] = None
