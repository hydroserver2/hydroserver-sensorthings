from itertools import groupby
from typing import Union, List
from hydrothings.engine import SensorThingsRequest
from hydrothings.schemas import EntityId
from .schemas import ObservationPostBody, ObservationDataArray

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
        } for datastream_id, observations in groupby(response['values'], key=lambda x: x['datastream_id'])
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
