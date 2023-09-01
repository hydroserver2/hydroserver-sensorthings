import re
import inspect
import sensorthings.components as core_components
import sensorthings.schemas as core_schemas
from ninja import Schema
from odata_query.grammar import ODataParser, ODataLexer
from django.http import HttpResponse
from pydantic import AnyHttpUrl
from typing import Literal, Union, List
from requests import Response
from sensorthings import settings


def lookup_component(
        input_value: str,
        input_type: Literal['snake_singular', 'snake_plural', 'camel_singular', 'camel_plural'],
        output_type: Literal['snake_singular', 'snake_plural', 'camel_singular', 'camel_plural']
) -> str:
    """
    Accepts a component name and type and returns an alternate form of the component name.

    Parameters
    ----------
    input_value : str
        The name of the component to look up.
    input_type: str
        The type of the component to lookup.
    output_type : str
        The type of the component to return.

    Returns
    -------
    str
        The matching component name.
    """

    st_components = [
        {
            'snake_singular': re.sub(r'(?<!^)(?=[A-Z])', '_', capability['SINGULAR_NAME']).lower(),
            'snake_plural': re.sub(r'(?<!^)(?=[A-Z])', '_', capability['NAME']).lower(),
            'camel_singular': capability['SINGULAR_NAME'],
            'camel_plural': capability['NAME']
        } for capability in settings.ST_CAPABILITIES
    ]

    return next((c[output_type] for c in st_components if c[input_type] == input_value))


def generate_response_codes(method: str, response_schema=None) -> dict:
    """
    Generates a dictionary of response codes for various request types.

    Parameters
    ----------
    method : str
        The SensorThings method the response is for.
    response_schema : class
        An alternate response schema to attach to the API.

    Returns
    -------
    dict
        A dictionary of response codes that can be returned for the given method.
    """

    if method == 'list':
        response_codes = {
            200: response_schema
        }
    elif method == 'get':
        response_codes = {
            200: response_schema,
            403: core_schemas.PermissionDenied,
            404: core_schemas.EntityNotFound
        }
    elif method == 'create':
        response_codes = {
            201: Union[None, List[AnyHttpUrl]],
            403: core_schemas.PermissionDenied
        }
    elif method == 'update':
        response_codes = {
            204: None,
            403: core_schemas.PermissionDenied,
            404: core_schemas.EntityNotFound
        }
    elif method == 'delete':
        response_codes = {
            204: None,
            403: core_schemas.PermissionDenied,
            404: core_schemas.EntityNotFound
        }
    else:
        response_codes = {}

    return response_codes


def serialize_response(response, response_model):
    """"""

    if not inspect.isclass(response_model):
        return response
    if not issubclass(response_model, Schema):
        return response

    new_model = response_model.__new__(response_model)

    fields_values = {}

    for name, field in response_model.__fields__.items():
        if name.endswith('_rel') and name in response.keys():
            if isinstance(response[name], list):
                fields_values[name] = [
                    serialize_response(
                        entity, getattr(core_components, field.field_info.extra.get('nested_class'))
                    ) for entity in response[name]
                ]
            else:
                fields_values[name] = serialize_response(
                    response[name], getattr(core_components, field.field_info.extra.get('nested_class'))
                )
        elif name in response.keys():
            if isinstance(response[name], list):
                fields_values[name] = [
                    serialize_response(fv, field.type_)
                    for fv in response[name]
                ]
            elif inspect.isclass(field.type_) and issubclass(field.type_, Schema):
                fields_values[name] = serialize_response(response[name], field.type_)
            else:
                fields_values[name] = response[name]

    object.__setattr__(new_model, '__dict__', fields_values)
    _fields_set = set(response.keys())
    object.__setattr__(new_model, '__fields_set__', _fields_set)

    new_model._init_private_attributes()

    return new_model


def entities_or_404(response, response_model):
    """"""

    if isinstance(response, Response):
        return response.status_code, response.content
    else:
        serialized_response = serialize_response(response, response_model).json(by_alias=True)
        return HttpResponse(content=serialized_response, status=200, content_type='application/json')


def entity_or_404(response, entity_id, response_model):
    """"""

    if isinstance(response, Response):
        return response.status_code, response.content
    elif response:
        serialized_response = serialize_response(response, response_model).json(by_alias=True)
        return HttpResponse(content=serialized_response, status=200, content_type='application/json')
    else:
        return 404, {'message': f'Record with ID {entity_id} does not exist.'}


def parse_query_params(
        query_params: dict,
        entity_chain: Union[List[tuple], None] = None,
        sort_datastream: bool = False
) -> dict:
    """
    Parses OData query parameters.

    This function converts OData query parameters in their string format to a dictionary of parameter objects that can
    be used to generate appropriate database queries.

    Parameters
    ----------
    query_params : dict
        A dictionary containing the raw string values of all query parameters passed with an API request.
    entity_chain : list
        A list of component/entity_id pairs representing a nested SensorThings request.
    sort_datastream : bool
        Adds a sort by datastream ID parameter if True (used in Observations requests to group by datastreams).

    Returns
    -------
    dict
        A dictionary containing all parsed query parameters.
    """

    if entity_chain:
        if query_params.get('filters'):
            query_params['filters'] += f' and {entity_chain[-1][0]}/id eq {entity_chain[-1][1]}'
        else:
            query_params['filters'] = f'{entity_chain[-1][0]}/id eq {entity_chain[-1][1]}'

    if query_params.get('filters'):
        query_params['filters'] = tokenize_filters(query_params['filters'])

    if sort_datastream is True:
        if query_params.get('order_by'):
            query_params['order_by'] += ', Datastreams/id'
        else:
            query_params['order_by'] = 'Datastreams/id'

    if query_params.get('order_by'):
        query_params['order_by'] = [
            {
                'field': order_field.strip().split(' ')[0],
                'direction': 'desc' if order_field.strip().endswith('desc') else 'asc'
            } for order_field in query_params['order_by'].split(',')
        ]

    if query_params.get('expand'):
        expanded_entities = [
            tokenize_expansion(entity)
            for entity in query_params['expand'].split(',')
        ]

        query_params['expand'] = expanded_entities

    return query_params


def tokenize_filters(filter_string):
    """"""

    lexer = ODataLexer()
    parser = ODataParser()

    return parser.parse(lexer.tokenize(filter_string))


def tokenize_expansion(entity):
    """"""

    nav_props = entity.split('/')

    if len(nav_props) == 0:
        return None

    nav_prop = nav_props[0]
    filter_search = re.findall(r'\(.*?\)', nav_prop)

    if filter_search and '$filter=' in filter_search[0]:
        nav_prop = nav_prop.split('(')[0]
        filters = tokenize_filters(filter_search[0][1:-1].replace('$filter=', ''))
    else:
        filters = None

    if len(nav_props) > 1:
        child_props = [tokenize_expansion('/'.join(nav_props[1:]))]
    else:
        child_props = []

    try:
        nav_prop = lookup_component(
            input_value=nav_prop,
            input_type='camel_plural',
            output_type='camel_singular'
        )
        array = True
    except:
        array = False

    return {
        'component': nav_prop,
        'array': array,
        'select': None,
        'filters': filters,
        'order_by': None,
        'pagination': None,
        'children': child_props
    }
