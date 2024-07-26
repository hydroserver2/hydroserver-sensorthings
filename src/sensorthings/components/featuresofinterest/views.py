from ninja import Query
from django.http import HttpResponse
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.http import SensorThingsHttpRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import (FeatureOfInterest, FeatureOfInterestPostBody, FeatureOfInterestPatchBody,
                      FeatureOfInterestListResponse, FeatureOfInterestGetResponse)


router = SensorThingsRouter(tags=['Features Of Interest'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_get('/FeaturesOfInterest', response_schema=FeatureOfInterestListResponse)
def list_features_of_interest(
        request: SensorThingsHttpRequest,
        params: ListQueryParams = Query(...)
):
    """
    Get a collection of Feature of Interest entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/properties" target="_blank">\
      Feature of Interest Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/relations" target="_blank">\
      Feature of Interest Relations</a>
    """

    return request.engine.list_entities(
        component=FeatureOfInterest,
        query_params=params.dict()
    )


@router.st_get(
    f'/FeaturesOfInterest({id_qualifier}{{feature_of_interest_id}}{id_qualifier})',
    response_schema=FeatureOfInterestGetResponse
)
def get_feature_of_interest(
        request: SensorThingsHttpRequest,
        feature_of_interest_id: id_type,
        params: GetQueryParams = Query(...)
):
    """
    Get a Feature of Interest entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/properties" target="_blank">\
      Feature of Interest Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/relations" target="_blank">\
      Feature of Interest Relations</a>
    """

    return request.engine.get_entity(
        component=FeatureOfInterest,
        entity_id=feature_of_interest_id,
        query_params=params.dict()
    )


@router.st_post('/FeaturesOfInterest')
def create_feature_of_interest(
        request: SensorThingsHttpRequest,
        response: HttpResponse,
        feature_of_interest: FeatureOfInterestPostBody
):
    """
    Create a new Feature of Interest entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/properties" target="_blank">\
      Feature of Interest Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/relations" target="_blank">\
      Feature of Interest Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    request.engine.create_entity(
        component=FeatureOfInterest,
        entity_body=feature_of_interest,
        response=response
    )

    return 201, None


@router.st_patch(f'/FeaturesOfInterest({id_qualifier}{{feature_of_interest_id}}{id_qualifier})')
def update_feature_of_interest(
        request: SensorThingsHttpRequest,
        feature_of_interest_id: id_type,
        feature_of_interest: FeatureOfInterestPatchBody
):
    """
    Update an existing Feature of Interest entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/properties" target="_blank">\
      Feature of Interest Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/relations" target="_blank">\
      Feature of Interest Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    request.engine.update_entity(
        component=FeatureOfInterest,
        entity_id=feature_of_interest_id,
        entity_body=feature_of_interest
    )

    return 204, None


@router.st_delete(f'/FeaturesOfInterest({id_qualifier}{{feature_of_interest_id}}{id_qualifier})')
def delete_feature_of_interest(
        request: SensorThingsHttpRequest,
        feature_of_interest_id: id_type
):
    """
    Delete a Feature of Interest entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete_entity(
        component=FeatureOfInterest,
        entity_id=feature_of_interest_id
    )

    return 204, None
