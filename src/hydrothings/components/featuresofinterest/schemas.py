from typing import TYPE_CHECKING, Literal, List
from pydantic import Field, HttpUrl
from geojson_pydantic import Feature
from ninja import Schema
from hydrothings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, NestedEntity
from hydrothings.validators import allow_partial

if TYPE_CHECKING:
    from hydrothings.components.observations.schemas import Observation


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


class FeatureOfInterestGetResponse(BaseGetResponse, FeatureOfInterestFields):
    observations_link: HttpUrl = Field(..., alias='Observations@iot.navigationLink')


class FeatureOfInterestListResponse(BaseListResponse):
    value: List[FeatureOfInterestGetResponse]
