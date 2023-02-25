import re
import hydrothings.schemas as core_schemas
from typing import Literal
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


def list_response_codes(response_schema):
    """"""

    return {
        200: response_schema
    }


def get_response_codes(response_schema):
    """"""

    return {
        200: response_schema,
        404: core_schemas.EntityNotFound
    }


def entity_or_404(response, entity_id):
    """"""

    if response:
        return 200, response
    else:
        return 404, {'message': f'Record with ID {entity_id} does not exist.'}
