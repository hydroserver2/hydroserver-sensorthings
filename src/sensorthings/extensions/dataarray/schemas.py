from typing import List, Literal, Optional, Union
from pydantic import Field
from ninja import Schema
from sensorthings.schemas import BaseListResponse, EntityId, ListQueryParams
from sensorthings.types import AnyHttpUrlString
from sensorthings.components.observations.schemas import (ObservationFields, ObservationGetResponse,
                                                          observationComponents)
from sensorthings import settings


id_type = settings.ST_API_ID_TYPE
observationResultFormats = Literal['dataArray']


class ObservationDataArrayFields(ObservationFields, EntityId):
    """
    Schema representing the fields of an observation in data array format.

    Attributes
    ----------
    datastream_id : id_type
        ID of the Datastream associated with the observation.
    feature_of_interest_id : Optional[id_type], optional
        ID of the Feature of Interest associated with the observation.
    """

    datastream_id: id_type = Field(..., alias='Datastream/id')
    feature_of_interest_id: Optional[id_type] = Field(None, alias='FeatureOfInterest/id')

    class Config:
        populate_by_name = True


class ObservationDataArrayResponse(Schema):
    """
    Response schema for an observation in data array format.

    Attributes
    ----------
    datastream : AnyHttpUrlString, optional
        Navigation link to the Datastream associated with the observation.
    components : List[observationComponents]
        List of observation components specified in the data array.
    data_array : List[list]
        List of lists representing the data array structure.
    """

    datastream: AnyHttpUrlString = Field(None, alias='Datastream@iot.navigationLink')
    components: List[observationComponents]
    data_array: List[list] = Field(..., alias='dataArray')

    class Config:
        populate_by_name = True


class ObservationDataArrayPostBody(Schema):
    """
    Schema for creating an observation in data array format.

    Attributes
    ----------
    datastream : EntityId
        ID of the Datastream associated with the observation.
    components : List[observationComponents]
        List of observation components specified in the data array.
    data_array : List[list]
        List of lists representing the data array structure.
    """

    datastream: EntityId = Field(..., alias='Datastream')
    components: List[observationComponents]
    data_array: List[list] = Field(..., alias='dataArray')

    class Config:
        populate_by_name = True


class ObservationQueryParams(ListQueryParams):
    """
    Query parameters schema for filtering observations.

    Attributes
    ----------
    result_format : Optional[observationResultFormats], optional
        Result format for the query, defaults to None.
    """

    result_format: Optional[observationResultFormats] = Field(None, alias='$resultFormat')

    class Config:
        populate_by_name = True


class ObservationListResponse(BaseListResponse):
    """
    Response schema for a list of observations.

    Attributes
    ----------
    value : Union[List[ObservationDataArrayResponse], List[ObservationGetResponse]]
        List containing either ObservationDataArrayResponse or ObservationGetResponse objects.
    """

    value: Union[List[ObservationDataArrayResponse], List[ObservationGetResponse]]
