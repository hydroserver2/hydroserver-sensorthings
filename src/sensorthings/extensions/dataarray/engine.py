from abc import ABCMeta, abstractmethod
from typing import Type, List, Union, TYPE_CHECKING
from itertools import groupby
from sensorthings.extensions.dataarray.schemas import ObservationDataArrayFields
from sensorthings import settings

if TYPE_CHECKING:
    from sensorthings.schemas import BaseComponent, BasePostBody


id_qualifier = settings.ST_API_ID_QUALIFIER


class DataArrayBaseEngine(metaclass=ABCMeta):

    @abstractmethod
    def create_observations(
            self,
            component: Type['BaseComponent'],
            entity_body: 'BasePostBody',
    ) -> List[str]:
        """
        Create Observations using data array format.

        Parameters:
        - component (Type['BaseComponent']): The type of component.
        - entity_body ('BasePostBody'): The entity body.

        Returns:
        - List[str]: The list of observation IDs.
        """

        pass

    def convert_to_data_array(
            self,
            response: dict,
            select: Union[str, None] = None
    ):
        """
        Convert Observations response to a data array.

        Parameters:
        - response (dict): The response dictionary.
        - select (Union[str, None]): Optional parameter to select specific fields.

        Returns:
        - dict: The converted data array response.
        """

        if select:
            selected_fields = [
                field[0] for field in ObservationDataArrayFields.model_fields.items()
                if field[1].alias in select.split(',')
            ]
            if 'id' in select.split(','):
                selected_fields = ['id'] + selected_fields
        else:
            selected_fields = [
                field for field in ObservationDataArrayFields.model_fields if field in ['phenomenon_time', 'result']
            ]

        response['value'] = [
            {
                'datastream_id': datastream_id,
                'datastream': f'{self.request.sensorthings_url}/'  # noqa
                              f'Datastreams({id_qualifier}{datastream_id}{id_qualifier})',
                'components': [
                    '@iot.id' if field == 'id' else ObservationDataArrayFields.model_fields[field].alias
                    for field in selected_fields
                ],
                'data_array': [
                    [
                        value for field, value in ObservationDataArrayFields(**observation).dict().items()
                        if field in selected_fields
                    ] for observation in observations
                ]
            } for datastream_id, observations in groupby(response['value'], key=lambda x: x['datastream_id'])
        ]

        return response
