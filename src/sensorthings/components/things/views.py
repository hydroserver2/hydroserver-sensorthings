from ninja import Query
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import ThingPostBody, ThingPatchBody, ThingListResponse, ThingGetResponse


router = SensorThingsRouter(tags=['Things'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_list('/Things', response_schemas=(ThingListResponse,), url_name='list_thing')
def list_things(
        request: SensorThingsRequest,
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
        request=request,
        query_params=params.dict()
    )


@router.st_get(f'/Things({id_qualifier}{{thing_id}}{id_qualifier})', response_schemas=(ThingGetResponse,))
def get_thing(
        request: SensorThingsRequest,
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

    return request.engine.get_entity(
        request=request,
        entity_id=thing_id,
        query_params=params.dict()
    )


@router.st_post('/Things')
def create_thing(
        request: SensorThingsRequest,
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

    return request.engine.create_entity(
        request=request,
        entity_body=thing
    )


@router.st_patch(f'/Things({id_qualifier}{{thing_id}}{id_qualifier})')
def update_thing(
        request: SensorThingsRequest,
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

    return request.engine.update_entity(
        request=request,
        entity_id=thing_id,
        entity_body=thing
    )


@router.delete(f'/Things({id_qualifier}{{thing_id}}{id_qualifier})')
def delete_thing(
        request: SensorThingsRequest,
        thing_id: id_type
):
    """
    Delete a Thing entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    return request.engine.delete_entity(
        request=request,
        entity_id=thing_id
    )
