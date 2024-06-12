from ninja import Query
from django.http import HttpResponse
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.http import SensorThingsHttpRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import (ObservedProperty, ObservedPropertyPostBody, ObservedPropertyPatchBody,
                      ObservedPropertyListResponse, ObservedPropertyGetResponse)


router = SensorThingsRouter(tags=['Observed Properties'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_list(
    '/ObservedProperties',
    response_schemas=(ObservedPropertyListResponse,),
    url_name='list_observed_property'
)
def list_observed_properties(
        request: SensorThingsHttpRequest,
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
        component=ObservedProperty,
        query_params=params.dict()
    )


@router.st_get(
    f'/ObservedProperties({id_qualifier}{{observed_property_id}}{id_qualifier})',
    response_schemas=(ObservedPropertyGetResponse,)
)
def get_observed_property(
        request: SensorThingsHttpRequest,
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
        component=ObservedProperty,
        entity_id=observed_property_id,
        query_params=params.dict()
    )


@router.st_post('/ObservedProperties')
def create_observed_property(
        request: SensorThingsHttpRequest,
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

    request.engine.create_entity(
        component=ObservedProperty,
        entity_body=observed_property,
        response=response
    )

    return 201, None


@router.st_patch(f'/ObservedProperties({id_qualifier}{{observed_property_id}}{id_qualifier})')
def update_observed_property(
        request: SensorThingsHttpRequest,
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

    request.engine.update_entity(
        component=ObservedProperty,
        entity_id=observed_property_id,
        entity_body=observed_property
    )

    return 204, None


@router.delete(f'/ObservedProperties({id_qualifier}{{observed_property_id}}{id_qualifier})')
def delete_observed_property(request: SensorThingsHttpRequest, observed_property_id: id_type):
    """
    Delete an Observed Property entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete_entity(
        component=ObservedProperty,
        entity_id=observed_property_id
    )

    return 204, None
