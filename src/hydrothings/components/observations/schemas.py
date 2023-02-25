from typing import TYPE_CHECKING, Literal, Union, List
from pydantic import Field, HttpUrl
from ninja import Schema
from hydrothings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, EntityId, \
    NestedEntity
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


class UnitOfMeasurement(Schema):
    name: str
    symbol: str
    definition: HttpUrl


class ObservationFields(Schema):
    phenomenon_time: Union[ISOTime, ISOInterval, None] = Field(..., alias='phenomenonTime')
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


class ObservationPostBody(BasePostBody, ObservationFields):
    datastream: Union[EntityId, NestedEntity] = Field(
        ..., alias='Datastream', nested_class='DatastreamPostBody'
    )
    feature_of_interest: Union[EntityId, NestedEntity] = Field(
        ..., alias='FeatureOfInterest', nested_class='FeatureOfInterestPostBody'
    )


@allow_partial
class ObservationPatchBody(BasePatchBody, ObservationFields):
    datastream: EntityId = Field(..., alias='Datastream')
    feature_of_interest: EntityId = Field(..., alias='FeatureOfInterest')


class ObservationGetResponse(ObservationFields, BaseGetResponse):
    datastream_link: HttpUrl = Field(..., alias='Datastream@iot.navigationLink')
    feature_of_interest_link: HttpUrl = Field(..., alias='FeatureOfInterest@iot.navigationLink')


class ObservationListResponse(BaseListResponse):
    value: List[ObservationGetResponse]
