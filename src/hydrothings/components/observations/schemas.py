from typing import TYPE_CHECKING, Literal, Union, List
from pydantic import Field, AnyHttpUrl
from ninja import Schema
from hydrothings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, EntityId, \
    NestedEntity, QueryParams
from hydrothings.extras.iso_types import ISOTime, ISOInterval
from hydrothings.validators import allow_partial

if TYPE_CHECKING:
    from hydrothings.components.datastreams.schemas import Datastream
    from hydrothings.components.featuresofinterest.schemas import FeatureOfInterest


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


class UnitOfMeasurement(Schema):
    name: str
    symbol: str
    definition: AnyHttpUrl


class ObservationFields(Schema):
    phenomenon_time: Union[ISOTime, ISOInterval, None] = Field(None, alias='phenomenonTime')
    result: str
    result_time: Union[ISOTime, None] = Field(..., alias='resultTime')
    result_quality: Union[str, None] = Field(None, alias='resultQuality')
    valid_time: Union[ISOInterval, None] = Field(None, alias='validTime')
    parameters: dict = {}


class ObservationRelations(Schema):
    datastream: 'Datastream'
    feature_of_interest: 'FeatureOfInterest'


class Observation(ObservationFields, ObservationRelations):
    pass


class ObservationDataArray(Schema):
    datastream: AnyHttpUrl = Field(..., alias='Datastream@iot.navigationLink')
    components: List[observationComponents]
    data_array: List[list] = Field(..., alias='dataArray')

    class Config:
        allow_population_by_field_name = True


class ObservationPostBody(BasePostBody, ObservationFields):
    datastream: Union[EntityId, NestedEntity] = Field(
        ..., alias='Datastream', nested_class='DatastreamPostBody'
    )
    feature_of_interest: Union[EntityId, NestedEntity, None] = Field(
        None, alias='FeatureOfInterest', nested_class='FeatureOfInterestPostBody'
    )


class ObservationDataArrayBody(Schema):
    datastream: EntityId = Field(..., alias='Datastream')
    components: List[observationComponents]
    data_array: List[list] = Field(..., alias='dataArray')


@allow_partial
class ObservationPatchBody(BasePatchBody, ObservationFields):
    datastream: EntityId = Field(..., alias='Datastream')
    feature_of_interest: EntityId = Field(..., alias='FeatureOfInterest')


class ObservationGetResponse(ObservationFields, BaseGetResponse):
    datastream_link: AnyHttpUrl = Field(..., alias='Datastream@iot.navigationLink')
    feature_of_interest_link: AnyHttpUrl = Field(..., alias='FeatureOfInterest@iot.navigationLink')

    class Config:
        allow_population_by_field_name = True


class ObservationListResponse(BaseListResponse):
    value: List[ObservationGetResponse]

    class Config:
        allow_population_by_field_name = True


class ObservationDataArrayResponse(BaseListResponse):
    value: List[ObservationDataArray]

    class Config:
        allow_population_by_field_name = True


class ObservationParams(QueryParams):
    result_format: Union[observationResultFormats, None] = Field(None, alias='$resultFormat')
