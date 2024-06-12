from ninja import Query
from django.http import HttpResponse
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.http import SensorThingsHttpRequest
from sensorthings.schemas import GetQueryParams, ListQueryParams
from sensorthings.components.datastreams.schemas import Datastream
from .schemas import (Observation, ObservationPostBody, ObservationPatchBody, ObservationListResponse,
                      ObservationGetResponse)


router = SensorThingsRouter(tags=['Observations'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_list(
    '/Observations',
    response_schemas=(ObservationListResponse,),
    url_name='list_observation'
)
def list_observations(
        request: SensorThingsHttpRequest,
        params: ListQueryParams = Query(...)
):
    """
    Get a collection of Observation entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    return request.engine.list_entities(
        component=Observation,
        query_params=params.dict()
    )


@router.st_get(
    f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})',
    response_schemas=(ObservationGetResponse,)
)
def get_observation(
        request: SensorThingsHttpRequest,
        observation_id: id_type,
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
        component=Observation,
        entity_id=observation_id,
        query_params=params.dict()
    )


@router.st_post('/Observations', url_name='create_observation')
def create_observation(
        request: SensorThingsHttpRequest,
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
        component=Observation,
        response=response,
        entity_body=observation
    )

    request.engine.update_related_components(
        component=Datastream, related_entity_id=observation.datastream.id
    )

    return 201, None


@router.st_patch(f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})')
def update_observation(
        request: SensorThingsHttpRequest,
        observation_id: id_type,
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

    request.engine.update_entity(
        component=Observation,
        entity_id=observation_id,
        entity_body=observation
    )

    return 204, None


@router.st_delete(f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})')
def delete_observation(
        request: SensorThingsHttpRequest,
        observation_id: id_type
):
    """
    Delete a Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete_entity(
        component=Observation,
        entity_id=observation_id
    )

    return 204, None
