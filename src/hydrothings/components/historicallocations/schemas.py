from typing import TYPE_CHECKING, List, Union
from datetime import datetime
from pydantic import Field, AnyHttpUrl
from ninja import Schema
from hydrothings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, EntityId, NestedEntity
from hydrothings.validators import allow_partial

if TYPE_CHECKING:
    from hydrothings.components.things.schemas import Thing
    from hydrothings.components.locations.schemas import Location


class HistoricalLocationFields(Schema):
    time: datetime


class HistoricalLocationRelations(Schema):
    thing: 'Thing'
    locations: List['Location']


class HistoricalLocation(HistoricalLocationFields, HistoricalLocationRelations):
    pass


class HistoricalLocationPostBody(BasePostBody, HistoricalLocationFields):
    thing: Union[EntityId, NestedEntity] = Field(
        ..., alias='Thing', nested_class='ThingPostBody'
    )
    locations: List[Union[EntityId, NestedEntity]] = Field(
        ..., alias='Locations', nested_class='LocationPostBody'
    )


@allow_partial
class HistoricalLocationPatchBody(HistoricalLocationFields, BasePatchBody):
    thing: EntityId = Field(..., alias='Thing')
    locations: List[EntityId] = Field(..., alias='Locations')


class HistoricalLocationGetResponse(BaseGetResponse, HistoricalLocationFields):
    thing_link: AnyHttpUrl = Field(..., alias='Thing@iot.navigationLink')
    historical_locations_link: AnyHttpUrl = Field(..., alias='Locations@iot.navigationLink')


class HistoricalLocationListResponse(BaseListResponse):
    value: List[HistoricalLocationGetResponse]
