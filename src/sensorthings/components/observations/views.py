import pytz
from ninja import Query
from typing import Union, List
from dateutil.parser import isoparse
from django.http import HttpResponse
from sensorthings.router import SensorThingsRouter
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import GetQueryParams
from .schemas import ObservationPostBody, ObservationPatchBody, ObservationListResponse, ObservationGetResponse, \
    ObservationParams, ObservationDataArrayResponse, ObservationDataArrayBody
from sensorthings.components.datastreams.schemas import DatastreamPatchBody


router = SensorThingsRouter(tags=['Observations'])


@router.st_list(
    '/Observations',
    response_schema=Union[ObservationListResponse, ObservationDataArrayResponse],
    url_name='list_observation'
)
def list_observations(
        request: SensorThingsRequest,
        params: ObservationParams = Query(...)
):
    """
    Get a collection of Observation entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    response = request.engine.list_entities(
        request=request,
        query_params=params.dict()
    )

    return response


@router.st_get('/Observations({observation_id})', response_schema=ObservationGetResponse)
def get_observation(
        request: SensorThingsRequest,
        observation_id: str,
        params: GetQueryParams = Query(...)
):
    """
    Get an Observation entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/properties" target="_blank">\
      Observation Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/observation/relations" target="_blank">\
      Observation Relations</a>
    """

    return request.engine.get_entity(
        request=request,
        entity_id=observation_id,
        query_params=params.dict()
    )


@router.st_post('/Observations')
def create_observation(
        request: SensorThingsRequest,
        response: HttpResponse,
        observation: Union[ObservationPostBody, List[ObservationDataArrayBody]]
):
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

    observation_links = None

    if isinstance(observation, ObservationPostBody):
        request.engine.create_entity(
            request=request,
            response=response,
            entity_body=observation
        )
    else:
        observation_links = request.engine.create_entity_bulk(
            request=request,
            entity_body=observation
        )

    for group in observation if isinstance(observation, list) else [observation]:

        first_observation = next(iter(request.engine.list_entities(
            request=request,
            query_params=ObservationParams(
                filters=f'Datastream/id eq \'{group.datastream.id}\'',
                expand='Datastream',
                order_by='phenomenonTime asc',
                top=1
            ).dict()
        )['value']), {})

        obs_phenomenon_begin_time_string = first_observation.get('phenomenon_time', None)
        obs_phenomenon_begin_time = isoparse(obs_phenomenon_begin_time_string).replace(tzinfo=pytz.UTC) if \
            obs_phenomenon_begin_time_string else None
        ds_phenomenon_begin_time_interval = first_observation.get('datastream_rel', {}).get('phenomenonTime', None)
        ds_phenomenon_begin_time = isoparse(ds_phenomenon_begin_time_interval.split('/')[0]) if \
            ds_phenomenon_begin_time_interval else None

        obs_result_begin_time_string = first_observation.get('result_time', None)
        obs_result_begin_time = isoparse(obs_result_begin_time_string).replace(tzinfo=pytz.UTC) if \
            obs_result_begin_time_string else None
        ds_result_begin_time_interval = first_observation.get('datastream_rel', {}).get('resultTime', None)
        ds_result_begin_time = isoparse(ds_result_begin_time_interval.split('/')[0]) if ds_result_begin_time_interval \
            else None

        if obs_phenomenon_begin_time and (not ds_phenomenon_begin_time or
                                          obs_phenomenon_begin_time < ds_phenomenon_begin_time):
            phenomenon_begin_time = obs_phenomenon_begin_time
        else:
            phenomenon_begin_time = ds_phenomenon_begin_time

        if obs_result_begin_time and (
                not ds_result_begin_time or obs_result_begin_time > ds_result_begin_time):
            result_begin_time = obs_result_begin_time
        else:
            result_begin_time = ds_result_begin_time

        last_observation = next(iter(request.engine.list_entities(
            request=request,
            query_params=ObservationParams(
                filters=f'Datastream/id eq \'{group.datastream.id}\'',
                expand='Datastream',
                order_by='phenomenonTime desc',
                top=1
            ).dict()
        )['value']), {})

        obs_phenomenon_end_time_string = last_observation.get('phenomenon_time', None)
        obs_phenomenon_end_time = isoparse(obs_phenomenon_end_time_string).replace(tzinfo=pytz.UTC) if \
            obs_phenomenon_end_time_string else None
        ds_phenomenon_end_time_interval = last_observation.get('datastream_rel', {}).get('phenomenonTime', None)
        ds_phenomenon_end_time = isoparse(ds_phenomenon_end_time_interval.split('/')[-1]) if \
            ds_phenomenon_end_time_interval else None

        obs_result_end_time_string = last_observation.get('result_time', None)
        obs_result_end_time = isoparse(obs_result_end_time_string).replace(tzinfo=pytz.UTC) if \
            obs_result_end_time_string else None
        ds_result_end_time_interval = last_observation.get('datastream_rel', {}).get('resultTime', None)
        ds_result_end_time = isoparse(ds_result_end_time_interval.split('/')[-1]) if ds_result_end_time_interval else None

        if obs_phenomenon_end_time and (not ds_phenomenon_end_time or obs_phenomenon_end_time > ds_phenomenon_end_time):
            phenomenon_end_time = obs_phenomenon_end_time
        else:
            phenomenon_end_time = ds_phenomenon_end_time

        if obs_result_end_time and (
                not ds_result_end_time or obs_result_end_time > ds_result_end_time):
            result_end_time = obs_result_end_time
        else:
            result_end_time = ds_result_end_time

        updated_phenomenon_time = request.engine.iso_time_interval(phenomenon_begin_time, phenomenon_end_time)
        updated_result_time = request.engine.iso_time_interval(result_begin_time, result_end_time)

        updated_phenomenon_time = updated_phenomenon_time.replace('+00:00', 'Z') if updated_phenomenon_time else None
        updated_result_time = updated_result_time.replace('+00:00', 'Z') if updated_result_time else None

        request.engine.update_entity(
            request=request,
            entity_id=group.datastream.id,
            entity_body=DatastreamPatchBody(
                phenomenon_time=updated_phenomenon_time,
                result_time=updated_result_time
            ),
            component='Datastream'
        )

    return 201, observation_links


@router.st_patch('/Observations({observation_id})')
def update_observation(
        request: SensorThingsRequest,
        observation_id: str,
        observation: ObservationPatchBody
):
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

    return request.engine.update_entity(
        request=request,
        entity_id=observation_id,
        entity_body=observation
    )


@router.st_delete('/Observations({observation_id})')
def delete_observation(
        request: SensorThingsRequest,
        observation_id: str
):
    """
    Delete a Observation entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    return request.engine.delete_entity(
        request=request,
        entity_id=observation_id
    )
