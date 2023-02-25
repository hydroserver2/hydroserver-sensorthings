from ninja import Router, Query
from django.http import HttpResponse
from hydrothings.engine import SensorThingsRequest
from hydrothings.schemas import Filters
from hydrothings.utils import entity_or_404, list_response_codes, get_response_codes
from .schemas import LocationPostBody, LocationPatchBody, LocationListResponse, LocationGetResponse


router = Router(tags=['Locations'])


@router.get(
    '/Locations',
    response=list_response_codes(LocationListResponse),
    by_alias=True,
    url_name='list_location'
)
def get_locations(request: SensorThingsRequest, filters: Filters = Query(...)):
    """
    Get a collection of Location entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/properties" target="_blank">\
      Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/relations" target="_blank">\
      Location Relations</a>
    """

    response = request.engine.list(**filters.dict())

    return 200, response


@router.get(
    '/Locations({location_id})',
    response=get_response_codes(LocationGetResponse),
    by_alias=True
)
def get_location(request: SensorThingsRequest, location_id: str):
    """
    Get a Location entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/properties" target="_blank">\
      Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/relations" target="_blank">\
      Location Relations</a>
    """

    response = request.engine.get(entity_id=location_id)

    return entity_or_404(response, location_id)


@router.post(
    '/Locations',
    response={201: None}
)
def create_location(request: SensorThingsRequest, response: HttpResponse, location: LocationPostBody):
    """
    Create a new Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/properties" target="_blank">\
      Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/relations" target="_blank">\
      Location Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    location_id = request.engine.create(
        entity_body=location
    )

    response['location'] = request.engine.get_ref(
        entity_id=location_id
    )

    return 201, None


@router.patch(
    '/Locations({location_id})',
    response={204: None}
)
def update_location(request: SensorThingsRequest, location_id: str, location: LocationPatchBody):
    """
    Update an existing Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/properties" target="_blank">\
      Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/relations" target="_blank">\
      Location Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    request.engine.update(
        entity_id=location_id,
        entity_body=location
    )

    return 204, None


@router.delete(
    '/Locations({location_id})',
    response={204: None}
)
def delete_location(request: SensorThingsRequest, location_id: str):
    """
    Delete a Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=location_id
    )

    return 204, None
