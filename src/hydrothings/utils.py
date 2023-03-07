import re
import hydrothings.schemas as core_schemas
from typing import Literal
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
            201: None
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
