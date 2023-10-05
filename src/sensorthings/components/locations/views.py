from ninja import Query
from sensorthings.router import SensorThingsRouter
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import LocationPostBody, LocationPatchBody, LocationListResponse, LocationGetResponse


router = SensorThingsRouter(tags=['Locations'])


@router.st_get('/Locations', response_schema=LocationListResponse, url_name='list_location')
def list_locations(
        request: SensorThingsRequest,
        params: ListQueryParams = Query(...)
):
    """
    Get a collection of Location entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/properties" target="_blank">\
      Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/relations" target="_blank">\
      Location Relations</a>
    """

    return request.engine.list_entities(
        request=request,
        query_params=params.dict()
    )


@router.get('/Locations({location_id})', response=LocationGetResponse)
def get_location(
        request: SensorThingsRequest,
        location_id: str,
        params: GetQueryParams = Query(...)
):
    """
    Get a Location entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/properties" target="_blank">\
      Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/location/relations" target="_blank">\
      Location Relations</a>
    """

    return request.engine.get_entity(
        request=request,
        entity_id=location_id,
        query_params=params.dict()
    )


@router.post('/Locations')
def create_location(
        request: SensorThingsRequest,
        location: LocationPostBody
):
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

    return request.engine.create_entity(
        request=request,
        entity_body=location
    )


@router.patch('/Locations({location_id})')
def update_location(
        request: SensorThingsRequest,
        location_id: str,
        location: LocationPatchBody
):
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

    return request.engine.update_entity(
        request=request,
        entity_id=location_id,
        entity_body=location
    )


@router.delete('/Locations({location_id})')
def delete_location(
        request: SensorThingsRequest,
        location_id: str
):
    """
    Delete a Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    return request.engine.delete_entity(
        request=request,
        entity_id=location_id
    )
