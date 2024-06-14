from typing import List, Union
from ninja import Query
from pydantic import AnyHttpUrl
from django.http import HttpResponse
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.http import SensorThingsHttpRequest
from sensorthings.schemas import PermissionDenied, EntityNotFound
from sensorthings.components.datastreams.schemas import Datastream
from sensorthings.components.observations.views import (get_observation, create_observation, update_observation,
                                                        delete_observation)
from sensorthings.components.observations.schemas import Observation
from sensorthings.extensions.dataarray.schemas import (ObservationDataArrayPostBody, ObservationQueryParams,
                                                       ObservationGetResponse,
                                                       ObservationListResponse)


router = SensorThingsRouter(tags=['Observations'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_list(
    '/Observations',
    response_schemas=(ObservationListResponse,),
    url_name='list_observation'
)
def list_observations(
        request: SensorThingsHttpRequest,
        params: ObservationQueryParams = Query(...)
):
    """
    Get a collection of Observation entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    response = request.engine.list_entities(
        component=Observation,
        query_params=params.dict()
    )

    if params.result_format == 'dataArray':
        response = request.engine.convert_to_data_array( # noqa
            response=response,
            select=params.select
        )

    return response


router.add_api_operation(
    f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})',
    methods=['GET'],
    response={
        200: Union[(ObservationGetResponse, str,)],
        403: PermissionDenied,
        404: EntityNotFound
    },
    view_func=get_observation,
    by_alias=True,
    exclude_unset=True,
)

router.add_api_operation(
    f'/Observations',
    methods=['POST'],
    response={
        201: Union[None, List[AnyHttpUrl]],
        403: PermissionDenied
    },
    view_func=create_observation
)

router.add_api_operation(
    f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})',
    methods=['PATCH'],
    response={
        204: None,
        403: PermissionDenied,
        404: EntityNotFound
    },
    view_func=update_observation
)

router.add_api_operation(
    f'/Observations({id_qualifier}{{observation_id}}{id_qualifier})',
    methods=['DELETE'],
    response={
        204: None,
        403: PermissionDenied,
        404: EntityNotFound
    },
    view_func=delete_observation
)


@router.st_post('/CreateObservations')
def create_observations(
        request: SensorThingsHttpRequest,
        response: HttpResponse,
        observations: List[ObservationDataArrayPostBody]
):
    """
    Create new Observation entities.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a> -
    <a href="https://docs.ogc.org/is/18-088/18-088.html#create-observation-dataarray" target="_blank">\
      Create Entities</a>
    """

    observation_links = request.engine.create_observations( # noqa
        response=response,
        entity_body=observations
    )

    datastream_ids = list(set([
        observation_group.datastream.id for observation_group in observations
    ]))

    for datastream_id in datastream_ids:
        request.engine.update_related_components(
            component=Datastream, related_entity_id=datastream_id
        )

    return 201, observation_links
