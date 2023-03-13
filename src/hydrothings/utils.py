import re
import hydrothings.schemas as core_schemas
from odata_query.grammar import ODataParser, ODataLexer
from pydantic import HttpUrl
from typing import Literal, Union, List
from requests import Response
from hydrothings import settings


def lookup_component(
        input_value: str,
        input_type: Literal['snake_singular', 'snake_plural', 'camel_singular', 'camel_plural'],
        output_type: Literal['snake_singular', 'snake_plural', 'camel_singular', 'camel_plural']
) -> str:
    """
    Accepts a component value and type and attempts to return an alternate form of the component name.

    :param input_value: The name of the component to lookup.
    :param input_type: The type of the component to lookup.
    :param output_type: The type of the component to return.
    :return output_value: The matching component name.
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


def generate_response_codes(method, response_schema=None):
    """"""

    if method == 'list':
        response_codes = {
            200: response_schema
        }
    elif method == 'get':
        response_codes = {
            200: response_schema,
            404: core_schemas.EntityNotFound
        }
    elif method == 'create':
        response_codes = {
            201: Union[None, List[HttpUrl]]
        }
    elif method == 'update':
        response_codes = {
            204: None,
            404: core_schemas.EntityNotFound
        }
    elif method == 'delete':
        response_codes = {
            204: None,
            404: core_schemas.EntityNotFound
        }
    else:
        response_codes = {}

    return response_codes


def entities_or_404(response):
    """"""

    if isinstance(response, Response):
        return response.status_code, response.content
    else:
        return 200, response


def entity_or_404(response, entity_id):
    """"""

    if isinstance(response, Response):
        return response.status_code, response.content
    elif response:
        return 200, response
    else:
        return 404, {'message': f'Record with ID {entity_id} does not exist.'}


def parse_query_params(query_params: dict, entity_chain=None, sort_datastream: bool = False) -> dict:
    """"""

    lexer = ODataLexer()
    parser = ODataParser()

    if entity_chain:
        if query_params.get('filters'):
            query_params['filters'] += f' and {entity_chain[-1][0]}/id eq {entity_chain[-1][1]}'
        else:
            query_params['filters'] = f'{entity_chain[-1][0]}/id eq {entity_chain[-1][1]}'

    if query_params.get('filters'):
        query_params['filters'] = parser.parse(lexer.tokenize(query_params['filters']))

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

    return query_params
