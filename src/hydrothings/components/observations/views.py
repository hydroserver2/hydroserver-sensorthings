from ninja import Router, Query
from django.http import HttpResponse
from hydrothings.engine import SensorThingsRequest
from hydrothings.schemas import Filters
from hydrothings.utils import entity_or_404, entities_or_404, list_response_codes, get_response_codes
from .schemas import ObservationPostBody, ObservationPatchBody, ObservationListResponse, ObservationGetResponse


router = Router(tags=['Observations'])


@router.get(
    '/Observations',
    response=list_response_codes(ObservationListResponse),
    by_alias=True,
    url_name='list_observation',
    exclude_none=True
)
def get_observations(request: SensorThingsRequest, filters: Filters = Query(...)):
    """
    Get a collection of Observation entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    response = request.engine.list(**filters.dict())

    return entities_or_404(response)


@router.get(
    '/Observations({observation_id})',
    response=get_response_codes(ObservationGetResponse),
    by_alias=True
)
def get_observation(request: SensorThingsRequest, observation_id: str):
    """
    Get an Observation entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    response = request.engine.get(entity_id=observation_id)

    return entity_or_404(response, observation_id)


@router.post(
    '/Observations',
    response={201: None}
)
def create_observation(request: SensorThingsRequest, response: HttpResponse, observation: ObservationPostBody):
    """
    Create a new Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    observation_id = request.engine.create(
        entity_body=observation
    )

    response['location'] = request.engine.get_ref(
        entity_id=observation_id
    )

    return 201, None


@router.patch(
    '/Observations({observation_id})',
    response={204: None}
)
def update_observation(request: SensorThingsRequest, observation_id: str, observation: ObservationPatchBody):
    """
    Update an existing Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    request.engine.update(
        entity_id=observation_id,
        entity_body=observation
    )

    return 204, None


@router.delete(
    '/Observations({observation_id})',
    response={204: None}
)
def delete_observation(request: SensorThingsRequest, observation_id: str):
    """
    Delete a Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=observation_id
    )

    return 204, None
