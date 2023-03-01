from ninja import Router, Query
from django.http import HttpResponse
from hydrothings.engine import SensorThingsRequest
from hydrothings.schemas import Filters
from hydrothings.utils import entity_or_404, entities_or_404, list_response_codes, get_response_codes
from .schemas import ThingPostBody, ThingPatchBody, ThingListResponse, ThingGetResponse


router = Router(tags=['Things'])


@router.get(
    '/Things',
    response=list_response_codes(ThingListResponse),
    by_alias=True,
    url_name='list_thing',
    exclude_none=True
)
def get_things(request: SensorThingsRequest, filters: Filters = Query(...)):
    """
    Get a collection of Thing entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/properties" target="_blank">\
      Thing Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/relations" target="_blank">\
      Thing Relations</a>
    """

    response = request.engine.list(**filters.dict())

    return entities_or_404(response)


@router.get(
    '/Things({thing_id})',
    response=get_response_codes(ThingGetResponse),
    by_alias=True
)
def get_thing(request: SensorThingsRequest, thing_id: str):
    """
    Get a Thing entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/properties" target="_blank">\
      Thing Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/thing/relations" target="_blank">\
      Thing Relations</a>
    """

    response = request.engine.get(entity_id=thing_id)

    return entity_or_404(response, thing_id)


@router.post(
    '/Things',
    response={201: None}
)
def create_thing(request: SensorThingsRequest, response: HttpResponse, thing: ThingPostBody):
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

    thing_id = request.engine.create(
        entity_body=thing
    )

    response['location'] = request.engine.get_ref(
        entity_id=thing_id
    )

    return 201, None


@router.patch(
    '/Things({thing_id})',
    response={204: None}
)
def update_thing(request: SensorThingsRequest, thing_id: str, thing: ThingPatchBody):
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

    request.engine.update(
        entity_id=thing_id,
        entity_body=thing
    )

    return 204, None


@router.delete(
    '/Things({thing_id})',
    response={204: None}
)
def delete_thing(request: SensorThingsRequest, thing_id: str):
    """
    Delete a Thing entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=thing_id
    )

    return 204, None
