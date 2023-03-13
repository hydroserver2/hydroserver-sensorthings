from ninja import Router, Query
from typing import Union, List
from django.http import HttpResponse
from hydrothings.engine import SensorThingsRequest
from hydrothings.utils import entity_or_404, entities_or_404, generate_response_codes, parse_query_params
from .schemas import ObservationPostBody, ObservationPatchBody, ObservationListResponse, ObservationGetResponse, \
    ObservationParams, ObservationDataArrayResponse, ObservationDataArrayBody
from .utils import convert_to_data_array, parse_data_array


router = Router(tags=['Observations'])


@router.get(
    '/Observations',
    response=generate_response_codes('list', Union[ObservationListResponse, ObservationDataArrayResponse]),
    by_alias=True,
    url_name='list_observation',
    exclude_none=True
)
def list_observations(request: SensorThingsRequest, params: ObservationParams = Query(...)):
    """
    Get a collection of Observation entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    query_params = params.dict()
    result_format = query_params.pop('result_format', None)

    response = request.engine.list(
        **parse_query_params(
            query_params=query_params,
            entity_chain=request.entity_chain,
            sort_datastream=True
        )
    )

    if result_format == 'dataArray':
        response = convert_to_data_array(request, response)

    return entities_or_404(response)


@router.get(
    '/Observations({observation_id})',
    response=generate_response_codes('get', ObservationGetResponse),
    by_alias=True
)
def get_observation(request: SensorThingsRequest, observation_id: str):
    """
    Get an Observation entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    response = request.engine.get(entity_id=observation_id)

    return entity_or_404(response, observation_id)


@router.post(
    '/Observations',
    response=generate_response_codes('create')
)
def create_observation(
        request: SensorThingsRequest,
        response: HttpResponse,
        observation: Union[ObservationPostBody, List[ObservationDataArrayBody]]
):
    """
    Create a new Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    if isinstance(observation, list):
        observations = parse_data_array(observation)

        if hasattr(request.engine, 'bulk_create'):
            observation_ids = request.engine.bulk_create(
                entity_bodies=observations
            )
            response_body = [
                request.engine.get_ref(
                    entity_id=observation_id
                ) for observation_id in observation_ids
            ]
        else:
            response_body = []
            for observation in observations:
                observation_id = request.engine.create(
                    entity_body=observation
                )
                response_body.extend(
                    request.engine.get_ref(
                        entity_id=observation_id
                    )
                )

    else:
        observation_id = request.engine.create(
            entity_body=observation
        )

        response['location'] = request.engine.get_ref(
            entity_id=observation_id
        )

        response_body = None

    return 201, response_body


@router.patch(
    '/Observations({observation_id})',
    response=generate_response_codes('update')
)
def update_observation(request: SensorThingsRequest, observation_id: str, observation: ObservationPatchBody):
    """
    Update an existing Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    request.engine.update(
        entity_id=observation_id,
        entity_body=observation
    )

    return 204, None


@router.delete(
    '/Observations({observation_id})',
    response=generate_response_codes('delete')
)
def delete_observation(request: SensorThingsRequest, observation_id: str):
    """
    Delete a Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=observation_id
    )

    return 204, None
