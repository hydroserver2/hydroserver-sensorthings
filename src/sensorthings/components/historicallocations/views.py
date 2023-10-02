from ninja import Router, Query
from django.http import HttpResponse
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from sensorthings.utils import entity_or_404, entities_or_404, generate_response_codes, parse_query_params
from .schemas import HistoricalLocationPostBody, HistoricalLocationPatchBody, HistoricalLocationListResponse, \
    HistoricalLocationGetResponse


router = Router(tags=['Historical Locations'])


@router.get(
    '/HistoricalLocations',
    response=generate_response_codes('list', HistoricalLocationListResponse),
    by_alias=True,
    exclude_unset=True,
    url_name='list_historical_location'
)
def list_historical_locations(request: SensorThingsRequest, params: ListQueryParams = Query(...)):
    """
    Get a collection of Historical Location entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/properties" target="_blank">\
      Historical Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/relations" target="_blank">\
      Historical Location Relations</a>
    """

    response = request.engine.list(
        **parse_query_params(
            query_params=params.dict(),
            entity_chain=request.entity_chain
        )
    )

    return entities_or_404(response, HistoricalLocationListResponse)


@router.get(
    '/HistoricalLocations({historical_location_id})',
    response=generate_response_codes('get', HistoricalLocationGetResponse),
    by_alias=True,
    exclude_unset=True
)
def get_historical_location(
        request: SensorThingsRequest,
        historical_location_id: str,
        params: GetQueryParams = Query(...)
):
    """
    Get a Historical Location entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/properties" target="_blank">\
      Historical Location Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/historical-location/relations" target="_blank">\
      Historical Location Relations</a>
    """

    response = request.engine.get(
        entity_id=historical_location_id,
        **parse_query_params(
            query_params=params.dict()
        )
    )
    return entity_or_404(response, historical_location_id, HistoricalLocationGetResponse)


@router.post(
    '/HistoricalLocations',
    response=generate_response_codes('create')
)
def create_historical_location(
        request: SensorThingsRequest,
        response: HttpResponse,
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

    historical_location_id = request.engine.create(
        entity_body=historical_location
    )

    response['location'] = request.engine.get_ref(
        entity_id=historical_location_id
    )

    return 201, None


@router.patch(
    '/HistoricalLocations({historical_location_id})',
    response=generate_response_codes('update')
)
def update_historical_location(
        request: SensorThingsRequest,
        historical_location_id: str,
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

    request.engine.update(
        entity_id=historical_location_id,
        entity_body=historical_location
    )

    return 204, None


@router.delete(
    '/HistoricalLocations({historical_location_id})',
    response=generate_response_codes('delete')
)
def delete_historical_location(request: SensorThingsRequest, historical_location_id: str):
    """
    Delete a Historical Location entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=historical_location_id
    )

    return 204, None
