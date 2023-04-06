from typing import TYPE_CHECKING, List
from pydantic import Field, AnyHttpUrl
from ninja import Schema
from hydrothings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, NestedEntity
from hydrothings.validators import allow_partial

if TYPE_CHECKING:
    from hydrothings.components.datastreams.schemas import Datastream


class ObservedPropertyFields(Schema):
    name: str
    definition: AnyHttpUrl
    description: str
    properties: dict = {}


class ObservedPropertyRelations(Schema):
    datastreams: List['Datastream'] = []


class ObservedProperty(ObservedPropertyFields, ObservedPropertyRelations):
    pass


class ObservedPropertyPostBody(BasePostBody, ObservedPropertyFields):
    datastreams: List[NestedEntity] = Field(
        [], alias='Datastreams', nested_class='DatastreamPostBody'
    )


@allow_partial
class ObservedPropertyPatchBody(BasePatchBody, ObservedPropertyFields):
    pass


class ObservedPropertyGetResponse(ObservedPropertyFields, BaseGetResponse):
    datastreams_link: AnyHttpUrl = Field(..., alias='Datastreams@iot.navigationLink')


class ObservedPropertyListResponse(BaseListResponse):
    value: List[ObservedPropertyGetResponse]
