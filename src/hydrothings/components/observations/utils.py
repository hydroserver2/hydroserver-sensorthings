from itertools import groupby
from typing import Union
from hydrothings.schemas import EntityId
from .schemas import ObservationPostBody

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


def convert_to_data_array(request, response, select: Union[list, None] = None):
    """"""

    if select:
        selected_fields = [
            field for field in fields if field[0] in select
        ]
    else:
        selected_fields = [
            field for field in fields if field[0] in ['result_time', 'result']
        ]

    datastream_url_template = f'{request.scheme}://{request.get_host()}{request.path[:-12]}Datastreams'

    response['value'] = [
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


def parse_data_array(observation):
    """"""

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
