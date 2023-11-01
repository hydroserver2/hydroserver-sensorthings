from ninja import Query
from typing import Union
from django.http import HttpResponse
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import GetQueryParams
from .utils import update_related_datastream
from .schemas import ObservationPostBody, ObservationPatchBody, ObservationListResponse, ObservationGetResponse, \
    ObservationParams, ObservationDataArrayResponse, ObservationDataArrayBody


router = SensorThingsRouter(tags=['Observations'])
id_qualifier = settings.ST_API_ID_QUALIFIER


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


@router.st_get(f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})', response_schema=ObservationGetResponse)
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


@router.st_post('/Observations')
def create_observation(
        request: SensorThingsRequest,
        response: HttpResponse,
        observation: ObservationPostBody
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

    request.engine.create_entity(
        request=request,
        response=response,
        entity_body=observation
    )

    update_related_datastream(request, observation)

    return 201, None


@router.st_post('/CreateObservations')
def create_observations(
        request: SensorThingsRequest,
        response: HttpResponse,
        observations: ObservationDataArrayBody
):
    """
    Create new Observation entities.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a> -
    <a href="https://docs.ogc.org/is/18-088/18-088.html#create-observation-dataarray" target="_blank">\
      Create Entities</a>
    """

    observation_links = request.engine.create_entity_bulk(
        request=request,
        entity_body=observations
    )

    for observation in observations:
        update_related_datastream(request, observation)

    return 201, observation_links


@router.st_patch(f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})')
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


@router.st_delete(f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})')
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
