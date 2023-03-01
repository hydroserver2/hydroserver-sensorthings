import hydrothings
import hydrothings.components as component_schemas
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.urls.exceptions import Http404
from django.http import HttpRequest
from hydrothings.utils import lookup_component
from hydrothings import settings


class SensorThingsMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request: HttpRequest) -> None:
        """
        Middleware for resolving nested components in SensorThings URLs.

        The SensorThings specification requires the server to handle nested resource paths and addresses to table
        properties (including values and reference links for the properties). This middleware checks the request URLs
        for these special cases, extracts any extra parameters from these URLs and attaches them to the request, and
        links the request to the correct view function by updating the request's path_info attribute.

        :param request: Django HttpRequest object.
        :return: None
        """

        try:
            resolved_path = resolve(request.path_info)
            if resolved_path.url_name != 'st_complex_handler':
                # Path is not part of the SensorThings app. Proceed normally.
                return None
        except StopIteration:
            # Path is not part of the SensorThings app. Proceed normally.
            return None

        if request.method != 'GET':
            # Nested components are only allowed on GET requests.
            raise Http404

        route_length = len(resolved_path.route.split('/'))
        path_components = request.path_info.split('/')[route_length:]
        path_prefix = '/'.join(request.path_info.split('/')[:route_length])
        component = None
        primary_component = None
        previous_component = None
        endpoint = None

        for i, raw_component in enumerate(path_components):
            path_info = f'{path_prefix}/{raw_component}'
            field_name = None

            try:
                resolved_path = resolve(path_info)
                if resolved_path.url_name is None:
                    # Sub-path may contain field names, or implicit links to related entities.
                    raise Http404
                if resolved_path.url_name.startswith('list'):
                    # This sub-path represents a collection of entities.
                    component = lookup_component(
                        input_value=resolved_path.url_name.replace('list_', ''),
                        input_type='snake_singular',
                        output_type='camel_singular'
                    )
                    field_name = lookup_component(
                        input_value=component,
                        input_type='camel_singular',
                        output_type='snake_plural'
                    )
                    primary_component = component
                    endpoint = f'{path_prefix}/{raw_component}'
                elif resolved_path.url_name.startswith('get'):
                    # This sub-path explicitly represents a single entity.
                    component = lookup_component(
                        input_value=resolved_path.url_name.replace('get_', ''),
                        input_type='snake_singular',
                        output_type='camel_singular'
                    )
                    field_name = lookup_component(
                        input_value=component,
                        input_type='camel_singular',
                        output_type='snake_singular'
                    )
                    primary_component = component
                    endpoint = f'{path_prefix}/{raw_component}'
            except Http404:
                try:
                    # This sub-path may be an implicit relation and needs to be converted to an explicit path.
                    component_plural = lookup_component(
                        input_value=raw_component,
                        input_type='camel_singular',
                        output_type='camel_plural'
                    )
                    field_name = lookup_component(
                        input_value=raw_component,
                        input_type='camel_singular',
                        output_type='snake_singular'
                    )
                    primary_component = raw_component
                    endpoint = f'{path_prefix}/{component_plural}(1)'  # TODO Need to lookup the associated id.
                except StopIteration:
                    # This sub-path may be a field name, $value, or $ref.
                    component = raw_component
                    field_name = lookup_component(
                        input_value=raw_component,
                        input_type='camel_singular',
                        output_type='snake_singular'
                    )

            if previous_component in [c['SINGULAR_NAME'] for c in settings.ST_CAPABILITIES]:
                # Check that this component is a valid child of the previous part of the path.
                if field_name not in getattr(component_schemas, previous_component).__fields__:
                    raise Http404
            elif previous_component in ['$value', '$ref']:
                # $value/$ref must be the last components of a path.
                raise Http404
            elif component == '$value':
                # The previous component must be a non-relational field.
                pass  # TODO Need to verify that the previous component is not a related field.
            elif component == '$ref':
                # The previous component must be a non-relational field.
                pass  # TODO Need to verify that the previous component is not a related field.
            else:
                pass  # TODO Need to figure out any other cases that need to be handled here.

            previous_component = component

        request.component_path = '/'.join(path_components)
        if endpoint:
            request.path_info = endpoint
        if primary_component in [c['SINGULAR_NAME'] for c in settings.ST_CAPABILITIES]:
            request.component = primary_component

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs) -> None:
        """
        Middleware for initializing a datastore engine for the request.

        This middleware generates a SensorThings engine object and attaches it to the request instance. The engine
        should include a connection to the associated database and methods for performing basic CRUD operations on that
        database and information model.

        :param request: Django HttpRequest object.
        :param view_func: The view function associated with this request.
        :param view_args: The arguments that will be passed to the view function.
        :param view_kwargs: The keyword arguments that will be passed to the view function.
        :return: None
        """

        if hasattr(getattr(view_func, '__self__', None), 'api'):
            st_api = view_func.__self__.api
            if isinstance(st_api, hydrothings.SensorThingsAPI):
                if not hasattr(request, 'component'):
                    request.component = None
                if not hasattr(request, 'component_path'):
                    request.component_path = request.path_info.split('/')[-1]
                request.engine = st_api.engine(
                    host=request.get_host(),
                    scheme=request.scheme,
                    path=request.path_info,
                    version=st_api.version,
                    component=request.component,
                    component_path=request.component_path
                )
