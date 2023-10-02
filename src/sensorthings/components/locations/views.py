from ninja import Router, Query
from django.http import HttpResponse
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from sensorthings.utils import entity_or_404, entities_or_404, generate_response_codes, parse_query_params
from .schemas import LocationPostBody, LocationPatchBody, LocationListResponse, LocationGetResponse


router = Router(tags=['Locations'])


@router.get(
    '/Locations',
    response=generate_response_codes('list', LocationListResponse),
    by_alias=True,
    exclude_unset=True,
    url_name='list_location'
)
def list_locations(request: SensorThingsRequest, params: ListQueryParams = Query(...)):
    """
    Get a collection of Location entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/properties" target="_blank">\
      Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/relations" target="_blank">\
      Location Relations</a>
    """

    response = request.engine.list(
        **parse_query_params(
            query_params=params.dict(),
            entity_chain=request.entity_chain
        )
    )

    return entities_or_404(response, LocationListResponse)


@router.get(
    '/Locations({location_id})',
    response=generate_response_codes('get', LocationGetResponse),
    by_alias=True,
    exclude_unset=True
)
def get_location(request: SensorThingsRequest, location_id: str, params: GetQueryParams = Query(...)):
    """
    Get a Location entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/properties" target="_blank">\
      Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/relations" target="_blank">\
      Location Relations</a>
    """

    response = request.engine.get(
        entity_id=location_id,
        **parse_query_params(
            query_params=params.dict()
        )
    )

    return entity_or_404(response, location_id, LocationGetResponse)


@router.post(
    '/Locations',
    response=generate_response_codes('create')
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
    response=generate_response_codes('update')
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
    response=generate_response_codes('delete')
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
