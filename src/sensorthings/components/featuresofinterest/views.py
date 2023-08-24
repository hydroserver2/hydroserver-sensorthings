from ninja import Router, Query
from django.http import HttpResponse
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from sensorthings.utils import entity_or_404, entities_or_404, generate_response_codes, parse_query_params
from .schemas import FeatureOfInterestPostBody, FeatureOfInterestPatchBody, FeatureOfInterestListResponse, \
    FeatureOfInterestGetResponse


router = Router(tags=['Features Of Interest'])


@router.get(
    '/FeaturesOfInterest',
    response=generate_response_codes('list', FeatureOfInterestListResponse),
    by_alias=True,
    exclude_unset=True,
    url_name='list_feature_of_interest'
)
def list_features_of_interest(request: SensorThingsRequest, params: ListQueryParams = Query(...)):
    """
    Get a collection of Feature of Interest entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/properties" target="_blank">\
      Feature of Interest Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/relations" target="_blank">\
      Feature of Interest Relations</a>
    """

    response = request.engine.list(
        **parse_query_params(
            query_params=params.dict(),
            entity_chain=request.entity_chain
        )
    )

    return entities_or_404(response, FeatureOfInterestListResponse)


@router.get(
    '/FeaturesOfInterest({feature_of_interest_id})',
    response=generate_response_codes('get', FeatureOfInterestGetResponse),
    by_alias=True,
    exclude_unset=True
)
def get_feature_of_interest(request, feature_of_interest_id: str, params: GetQueryParams = Query(...)):
    """
    Get a Feature of Interest entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/properties" target="_blank">\
      Feature of Interest Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/relations" target="_blank">\
      Feature of Interest Relations</a>
    """

    response = request.engine.get(
        entity_id=feature_of_interest_id,
        **parse_query_params(
            query_params=params.dict()
        )
    )

    return entity_or_404(response, feature_of_interest_id, FeatureOfInterestGetResponse)


@router.post(
    '/FeaturesOfInterest',
    response=generate_response_codes('create')
)
def create_feature_of_interest(
        request: SensorThingsRequest,
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

    feature_of_interest_id = request.engine.create(
        entity_body=feature_of_interest
    )

    response['location'] = request.engine.get_ref(
        entity_id=feature_of_interest_id
    )

    return 201, None


@router.patch(
    '/FeaturesOfInterest({feature_of_interest_id})',
    response=generate_response_codes('update')
)
def update_feature_of_interest(
        request: SensorThingsRequest,
        feature_of_interest_id: str,
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

    request.engine.update(
        entity_id=feature_of_interest_id,
        entity_body=feature_of_interest
    )

    return 204, None


@router.delete(
    '/FeaturesOfInterest({feature_of_interest_id})',
    response=generate_response_codes('delete')
)
def delete_feature_of_interest(request: SensorThingsRequest, feature_of_interest_id: str):
    """
    Delete a Feature of Interest entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=feature_of_interest_id
    )

    return 204, None
