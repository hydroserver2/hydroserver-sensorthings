from uuid import UUID
from typing import TYPE_CHECKING, Literal, Union, List
from pydantic import Field, AnyHttpUrl
from ninja import Schema
from sensorthings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, EntityId, \
    NestedEntity, ListQueryParams
from sensorthings.extras.iso_types import ISOTime, ISOInterval
from sensorthings.validators import allow_partial

if TYPE_CHECKING:
    from sensorthings.components.datastreams.schemas import Datastream
    from sensorthings.components.featuresofinterest.schemas import FeatureOfInterest


observationTypes = Literal[
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CategoryObservation',
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation',
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation',
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_TruthObservation'
]


observationComponents = Literal[
    'id', 'phenomenonTime', 'result', 'resultTime', 'resultQuality', 'validTime', 'parameters', 'FeatureOfInterest/id'
]

observationResultFormats = Literal['dataArray']


class ObservationFields(Schema):
    phenomenon_time: Union[ISOTime, ISOInterval] = Field(..., alias='phenomenonTime')
    result: float
    result_time: Union[ISOTime, None] = Field(None, alias='resultTime')
    result_quality: dict = Field({}, alias='resultQuality')
    valid_time: Union[ISOInterval, None] = Field(None, alias='validTime')
    parameters: dict = {}


class ObservationRelations(Schema):
    datastream: 'Datastream'
    feature_of_interest: 'FeatureOfInterest'


class Observation(ObservationFields, ObservationRelations):
    pass


class ObservationPostBody(BasePostBody, ObservationFields):
    datastream: Union[EntityId, NestedEntity] = Field(
        ..., alias='Datastream', nested_class='DatastreamPostBody'
    )
    feature_of_interest: Union[EntityId, NestedEntity, None] = Field(
        None, alias='FeatureOfInterest', nested_class='FeatureOfInterestPostBody'
    )


@allow_partial
class ObservationPatchBody(BasePatchBody, ObservationFields):
    datastream: EntityId = Field(..., alias='Datastream')
    feature_of_interest: EntityId = Field(..., alias='FeatureOfInterest')


class ObservationGetResponse(ObservationFields, BaseGetResponse):
    datastream_link: AnyHttpUrl = Field(None, alias='Datastream@iot.navigationLink')
    datastream_rel: NestedEntity = Field(None, alias='Datastream', nested_class='DatastreamGetResponse')
    feature_of_interest_link: AnyHttpUrl = Field(None, alias='FeatureOfInterest@iot.navigationLink')
    feature_of_interest_rel: NestedEntity = Field(
        None,
        alias='FeatureOfInterest',
        nested_class='FeatureOfInterestGetResponse'
    )


class ObservationListResponse(BaseListResponse):
    value: List[ObservationGetResponse]


class ObservationDataArrayFields(ObservationFields):
    datastream_id: Union[UUID, str] = Field(..., alias='Datastream/id')
    feature_of_interest_id: Union[UUID, str] = Field(None, alias='FeatureOfInterest/id')

    class Config:
        allow_population_by_field_name = True


class ObservationDataArray(Schema):
    datastream: AnyHttpUrl = Field(None, alias='Datastream@iot.navigationLink')
    components: List[observationComponents]
    data_array: List[list] = Field(..., alias='dataArray')

    class Config:
        allow_population_by_field_name = True


class ObservationDataArrayBody(Schema):
    datastream: EntityId = Field(..., alias='Datastream')
    components: List[observationComponents]
    data_array: List[list] = Field(..., alias='dataArray')


class ObservationDataArrayResponse(BaseListResponse):
    value: List[ObservationDataArray]


class ObservationParams(ListQueryParams):
    result_format: Union[observationResultFormats, None] = Field(None, alias='$resultFormat')
