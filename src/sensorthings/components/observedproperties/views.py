from ninja import Query
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import ObservedPropertyPostBody, ObservedPropertyPatchBody, ObservedPropertyListResponse, \
    ObservedPropertyGetResponse


router = SensorThingsRouter(tags=['Observed Properties'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_list(
    '/ObservedProperties',
    response_schemas=(ObservedPropertyListResponse,),
    url_name='list_observed_property'
)
def list_observed_properties(
        request: SensorThingsRequest,
        params: ListQueryParams = Query(...)
):
    """
    Get a collection of Observed Property entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/properties" target="_blank">\
      Observed Property Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/relations" target="_blank">\
      Observed Property Relations</a>
    """

    return request.engine.list_entities(
        request=request,
        query_params=params.dict()
    )


@router.st_get(
    f'/ObservedProperties({id_qualifier}{{observed_property_id}}{id_qualifier})',
    response_schemas=(ObservedPropertyGetResponse,)
)
def get_observed_property(
        request: SensorThingsRequest,
        observed_property_id: id_type,
        params: GetQueryParams = Query(...)
):
    """
    Get an Observed Property entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/properties" target="_blank">\
      Observed Property Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observed-property/relations" target="_blank">\
      Observed Property Relations</a>
    """

    return request.engine.get_entity(
        request=request,
        entity_id=observed_property_id,
        query_params=params.dict()
    )


@router.st_post('/ObservedProperties')
def create_observed_property(
        request: SensorThingsRequest,
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

    return request.engine.create_entity(
        request=request,
        entity_body=observed_property
    )


@router.st_patch(f'/ObservedProperties({id_qualifier}{{observed_property_id}}{id_qualifier})')
def update_observed_property(
        request: SensorThingsRequest,
        observed_property_id: id_type,
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

    return request.engine.update_entity(
        request=request,
        entity_id=observed_property_id,
        entity_body=observed_property
    )


@router.delete(f'/ObservedProperties({id_qualifier}{{observed_property_id}}{id_qualifier})')
def delete_observed_property(request: SensorThingsRequest, observed_property_id: id_type):
    """
    Delete an Observed Property entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    return request.engine.delete_entity(
        request=request,
        entity_id=observed_property_id
    )
