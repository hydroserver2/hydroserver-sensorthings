from ninja import Query
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import HistoricalLocationPostBody, HistoricalLocationPatchBody, HistoricalLocationListResponse, \
    HistoricalLocationGetResponse


router = SensorThingsRouter(tags=['Historical Locations'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_list(
    '/HistoricalLocations',
    response_schema=HistoricalLocationListResponse,
    url_name='list_historical_location'
)
def list_historical_locations(
        request: SensorThingsRequest,
        params: ListQueryParams = Query(...)
):
    """
    Get a collection of Historical Location entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/properties" target="_blank">\
      Historical Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/relations" target="_blank">\
      Historical Location Relations</a>
    """

    return request.engine.list_entities(
        request=request,
        query_params=params.dict()
    )


@router.st_get(
    f'/HistoricalLocations({id_qualifier}{{historical_location_id}}{id_qualifier})',
    response_schema=HistoricalLocationGetResponse
)
def get_historical_location(
        request: SensorThingsRequest,
        historical_location_id: id_type,
        params: GetQueryParams = Query(...)
):
    """
    Get a Historical Location entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/properties" target="_blank">\
      Historical Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/relations" target="_blank">\
      Historical Location Relations</a>
    """

    return request.engine.get_entity(
        request=request,
        entity_id=historical_location_id,
        query_params=params.dict()
    )


@router.st_post('/HistoricalLocations')
def create_historical_location(
        request: SensorThingsRequest,
        historical_location: HistoricalLocationPostBody
):
    """
    Create a new Historical Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/properties" target="_blank">\
      Historical Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/relations" target="_blank">\
      Historical Location Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    return request.engine.create_entity(
        request=request,
        entity_body=historical_location
    )


@router.st_patch(f'/HistoricalLocations({id_qualifier}{{historical_location_id}}{id_qualifier})')
def update_historical_location(
        request: SensorThingsRequest,
        historical_location_id: id_type,
        historical_location: HistoricalLocationPatchBody
):
    """
    Update an existing Historical Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/properties" target="_blank">\
      Historical Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/relations" target="_blank">\
      Historical Location Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    return request.engine.update_entity(
        request=request,
        entity_id=historical_location_id,
        entity_body=historical_location
    )


@router.st_delete(f'/HistoricalLocations({id_qualifier}{{historical_location_id}}{id_qualifier})')
def delete_historical_location(request: SensorThingsRequest, historical_location_id: id_type):
    """
    Delete a Historical Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    return request.engine.delete_entity(
        request=request,
        entity_id=historical_location_id
    )
