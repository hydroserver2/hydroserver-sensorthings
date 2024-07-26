from ninja import Query
from django.http import HttpResponse
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.http import SensorThingsHttpRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import Location, LocationPostBody, LocationPatchBody, LocationListResponse, LocationGetResponse


router = SensorThingsRouter(tags=['Locations'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_get('/Locations', response_schema=LocationListResponse, url_name='list_location')
def list_locations(
        request: SensorThingsHttpRequest,
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
        component=Location,
        query_params=params.dict()
    )


@router.st_get(f'/Locations({id_qualifier}{{location_id}}{id_qualifier})', response_schema=LocationGetResponse)
def get_location(
        request: SensorThingsHttpRequest,
        location_id: id_type,
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
        component=Location,
        entity_id=location_id,
        query_params=params.dict()
    )


@router.post('/Locations')
def create_location(
        request: SensorThingsHttpRequest,
        response: HttpResponse,
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

    request.engine.create_entity(
        component=Location,
        entity_body=location,
        response=response
    )

    return 201, None


@router.patch(f'/Locations({id_qualifier}{{location_id}}{id_qualifier})')
def update_location(
        request: SensorThingsHttpRequest,
        location_id: id_type,
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

    request.engine.update_entity(
        component=Location,
        entity_id=location_id,
        entity_body=location
    )

    return 204, None


@router.delete(f'/Locations({id_qualifier}{{location_id}}{id_qualifier})')
def delete_location(
        request: SensorThingsHttpRequest,
        location_id: id_type
):
    """
    Delete a Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete_entity(
        component=Location,
        entity_id=location_id
    )

    return 204, None
