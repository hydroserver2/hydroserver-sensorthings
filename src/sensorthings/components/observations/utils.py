import pytz
from itertools import groupby
from typing import Union, List
from dateutil.parser import isoparse
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import EntityId
from sensorthings.components.datastreams.schemas import DatastreamPatchBody
from .schemas import ObservationPostBody, ObservationParams, ObservationDataArray

fields = [
    ('id', 'id',),
    ('phenomenon_time', 'phenomenonTime',),
    ('result_time', 'resultTime',),
    ('result', 'result',),
    ('result_quality', 'resultQuality',),
    ('valid_time', 'validTime',),
    ('parameters', 'parameters',),
    ('feature_of_interest', 'FeatureOfInterest/id',)
]


def convert_to_data_array(
        request: SensorThingsRequest,
        response: dict,
        select: Union[list, None] = None
) -> dict:
    """
    Converts an Observations response dictionary to the dataArray format.

    Parameters
    ----------
    request : SensorThingsRequest
        The SensorThingsRequest object associated with the response.
    response : dict
        A SensorThings response dictionary.
    select
        A list of fields that should be included in the response.

    Returns
    -------
    dict
        A SensorThings response dictionary formatted as a dataArray.
    """

    if select:
        selected_fields = [
            field for field in fields if field[0] in select
        ]
    else:
        selected_fields = [
            field for field in fields if field[0] in ['result_time', 'result']
        ]

    datastream_url_template = f'{request.scheme}://{request.get_host()}{request.path[:-12]}Datastreams'

    response['values'] = [
        {
            'datastream': f'{datastream_url_template}({datastream_id})',
            'components': [
                field[1] for field in selected_fields
            ],
            'data_array': [
                [
                    observation[field[0]] for field in selected_fields
                ] for observation in observations
            ]
        } for datastream_id, observations in groupby(response['value'], key=lambda x: x['datastream_id'])
    ]

    return response


def parse_data_array(
        observation: List[ObservationDataArray]
) -> List[ObservationPostBody]:
    """
    Parses an ObservationDataArray object.

    Converts an ObservationDataArray object to a list of ObservationPostBody objects that can be loaded by the
    SensorThings engine.

    Parameters
    ----------
    observation: ObservationDataArray
        An ObservationDataArray object.

    Returns
    -------
    List[ObservationPostBody]
        A list of ObservationPostBody objects.
    """

    observations = []

    for datastream in observation:
        datastream_fields = [
            (field[0], field[1], get_field_index(datastream.components, field[1]),) for field in fields
        ]

        observations.extend([
            ObservationPostBody(
                datastream=datastream.datastream,
                **{
                    datastream_field[0]: entity[datastream_field[2]]
                    if datastream_field[0] != 'feature_of_interest'
                    else EntityId(
                        id=entity[datastream_field[2]]
                    )
                    for datastream_field in datastream_fields if datastream_field[2] is not None
                }
            ) for entity in datastream.data_array
        ])

    return observations


def get_field_index(components, field):
    """"""

    try:
        return components.index(field)
    except ValueError:
        return None


def update_related_datastream(request, observation):
    first_observation = next(iter(request.engine.list_entities(
        request=request,
        query_params=ObservationParams(
            filters=f'Datastream/id eq \'{observation.datastream.id}\'',
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
            filters=f'Datastream/id eq \'{observation.datastream.id}\'',
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
        entity_id=observation.datastream.id,
        entity_body=DatastreamPatchBody(
            phenomenon_time=updated_phenomenon_time,
            result_time=updated_result_time
        ),
        component='Datastream'
    )
