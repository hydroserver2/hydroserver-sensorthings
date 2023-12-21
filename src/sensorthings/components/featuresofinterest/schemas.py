from typing import TYPE_CHECKING, Literal, List
from pydantic import Field, AnyHttpUrl
from geojson_pydantic import Feature
from ninja import Schema
from sensorthings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, NestedEntity
from sensorthings.validators import allow_partial

if TYPE_CHECKING:
    from sensorthings.components.observations.schemas import Observation


featureEncodingTypes = Literal['application/geo+json']


class FeatureOfInterestFields(Schema):
    name: str
    description: str
    encoding_type: featureEncodingTypes = Field(..., alias='encodingType')
    feature: Feature
    properties: dict = {}


class FeatureOfInterestRelations(Schema):
    observations: List['Observation'] = []


class FeatureOfInterest(FeatureOfInterestFields, FeatureOfInterestRelations):
    pass


class FeatureOfInterestPostBody(BasePostBody, FeatureOfInterestFields):
    observations: List[NestedEntity] = Field(
        [], alias='Observations', nested_class='ObservationPostBody'
    )


@allow_partial
class FeatureOfInterestPatchBody(FeatureOfInterestFields, BasePatchBody):
    pass


@allow_partial
class FeatureOfInterestGetResponse(FeatureOfInterestFields, BaseGetResponse):
    observations_link: AnyHttpUrl = Field(None, alias='Observations@iot.navigationLink')
    observations_rel: List[NestedEntity] = Field(None, alias='Observations', nested_class='ObservationGetResponse')


class FeatureOfInterestListResponse(BaseListResponse):
    value: List[FeatureOfInterestGetResponse]
