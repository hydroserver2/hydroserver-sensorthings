from ninja import Query
from typing import Union, List
from sensorthings.router import SensorThingsRouter
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import GetQueryParams
from .schemas import ObservationPostBody, ObservationPatchBody, ObservationListResponse, ObservationGetResponse, \
    ObservationParams, ObservationDataArrayResponse, ObservationDataArrayBody


router = SensorThingsRouter(tags=['Observations'])


@router.st_list(
    '/Observations',
    response_schema=Union[ObservationListResponse, ObservationDataArrayResponse],
    url_name='list_observation'
)
def list_observations(
        request: SensorThingsRequest,
        params: ObservationParams = Query(...)
):
    """
    Get a collection of Observation entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    response = request.engine.list_entities(
        request=request,
        query_params=params.dict()
    )

    return response


@router.st_get('/Observations({observation_id})', response_schema=ObservationGetResponse)
def get_observation(
        request: SensorThingsRequest,
        observation_id: str,
        params: GetQueryParams = Query(...)
):
    """
    Get an Observation entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    return request.engine.get_entity(
        request=request,
        entity_id=observation_id,
        query_params=params.dict()
    )


@router.post('/Observations')
def create_observation(
        request: SensorThingsRequest,
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

    return request.engine.create_entity(
        request=request,
        entity_body=observation
    )


@router.patch('/Observations({observation_id})')
def update_observation(
        request: SensorThingsRequest,
        observation_id: str,
        observation: ObservationPatchBody
):
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

    return request.engine.update_entity(
        request=request,
        entity_id=observation_id,
        entity_body=observation
    )


@router.delete('/Observations({observation_id})')
def delete_observation(
        request: SensorThingsRequest,
        observation_id: str
):
    """
    Delete a Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    return request.engine.delete_entity(
        request=request,
        entity_id=observation_id
    )
