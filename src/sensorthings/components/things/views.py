from ninja import Query
from django.http import HttpResponse
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.http import SensorThingsHttpRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import Thing, ThingPostBody, ThingPatchBody, ThingListResponse, ThingGetResponse


router = SensorThingsRouter(tags=['Things'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_list('/Things', response_schema=ThingListResponse, url_name='list_thing')
def list_things(
        request: SensorThingsHttpRequest,
        params: ListQueryParams = Query(...)
):
    """
    Get a collection of Thing entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/properties" target="_blank">\
      Thing Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/relations" target="_blank">\
      Thing Relations</a>
    """

    return request.engine.list_entities(
        component=Thing,
        query_params=params.dict()
    )


@router.st_get(f'/Things({id_qualifier}{{thing_id}}{id_qualifier})', response_schema=ThingGetResponse)
def get_thing(
        request: SensorThingsHttpRequest,
        thing_id: id_type,
        params: GetQueryParams = Query(...)
):
    """
    Get a Thing entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/properties" target="_blank">\
      Thing Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/relations" target="_blank">\
      Thing Relations</a>
    """

    response = request.engine.get_entity(
        component=Thing,
        entity_id=thing_id,
        query_params=params.dict()
    )

    return response


@router.st_post('/Things')
def create_thing(
        request: SensorThingsHttpRequest,
        response: HttpResponse,
        thing: ThingPostBody
):
    """
    Create a new Thing entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/properties" target="_blank">\
      Thing Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/relations" target="_blank">\
      Thing Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    request.engine.create_entity(
        component=Thing,
        entity_body=thing,
        response=response
    )

    return 201, None


@router.st_patch(f'/Things({id_qualifier}{{thing_id}}{id_qualifier})')
def update_thing(
        request: SensorThingsHttpRequest,
        thing_id: id_type,
        thing: ThingPatchBody
):
    """
    Update an existing Thing entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/properties" target="_blank">\
      Thing Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/relations" target="_blank">\
      Thing Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    request.engine.update_entity(
        component=Thing,
        entity_id=thing_id,
        entity_body=thing
    )

    return 204, None


@router.delete(f'/Things({id_qualifier}{{thing_id}}{id_qualifier})')
def delete_thing(
        request: SensorThingsHttpRequest,
        thing_id: id_type
):
    """
    Delete a Thing entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete_entity(
        component=Thing,
        entity_id=thing_id
    )

    return 204, None
