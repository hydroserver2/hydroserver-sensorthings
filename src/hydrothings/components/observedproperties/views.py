from ninja import Router, Query
from django.http import HttpResponse
from hydrothings.engine import SensorThingsRequest
from hydrothings.schemas import ListQueryParams, GetQueryParams
from hydrothings.utils import entity_or_404, entities_or_404, generate_response_codes, parse_query_params
from .schemas import ObservedPropertyPostBody, ObservedPropertyPatchBody, ObservedPropertyListResponse, \
    ObservedPropertyGetResponse


router = Router(tags=['Observed Properties'])


@router.get(
    '/ObservedProperties',
    response=generate_response_codes('list', ObservedPropertyListResponse),
    by_alias=True,
    url_name='list_observed_property',
    exclude_unset=True
)
def list_observed_properties(request: SensorThingsRequest, params: ListQueryParams = Query(...)):
    """
    Get a collection of Observed Property entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/properties" target="_blank">\
      Observed Property Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/relations" target="_blank">\
      Observed Property Relations</a>
    """

    response = request.engine.list(
        **parse_query_params(
            query_params=params.dict(),
            entity_chain=request.entity_chain
        )
    )

    return entities_or_404(response, ObservedPropertyListResponse)


@router.get(
    '/ObservedProperties({observed_property_id})',
    response=generate_response_codes('get', ObservedPropertyGetResponse),
    by_alias=True,
    exclude_unset=True
)
def get_observed_property(request, observed_property_id: str, params: GetQueryParams = Query(...)):
    """
    Get an Observed Property entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/properties" target="_blank">\
      Observed Property Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/relations" target="_blank">\
      Observed Property Relations</a>
    """

    response = request.engine.get(
        entity_id=observed_property_id,
        **parse_query_params(
            query_params=params.dict()
        )
    )

    return entity_or_404(response, observed_property_id, ObservedPropertyGetResponse)


@router.post(
    '/ObservedProperties',
    response=generate_response_codes('create')
)
def create_observed_property(
        request: SensorThingsRequest,
        response: HttpResponse,
        observed_property: ObservedPropertyPostBody
):
    """
    Create a new Observed Property entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/properties" target="_blank">\
      Observed Property Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/relations" target="_blank">\
      Observed Property Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    observed_property_id = request.engine.create(
        entity_body=observed_property
    )

    response['location'] = request.engine.get_ref(
        entity_id=observed_property_id
    )

    return 201, None


@router.patch(
    '/ObservedProperties({observed_property_id})',
    response=generate_response_codes('update')
)
def update_observed_property(
        request: SensorThingsRequest,
        observed_property_id: str,
        observed_property: ObservedPropertyPatchBody
):
    """
    Update an existing Observed Property entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/properties" target="_blank">\
      Thing Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/relations" target="_blank">\
      Thing Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    request.engine.update(
        entity_id=observed_property_id,
        entity_body=observed_property
    )

    return 204, None


@router.delete(
    '/ObservedProperties({observed_property_id})',
    response=generate_response_codes('delete')
)
def delete_observed_property(request: SensorThingsRequest, observed_property_id: str):
    """
    Delete an Observed Property entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=observed_property_id
    )

    return 204, None
