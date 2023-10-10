from typing import TYPE_CHECKING, List, Union
from datetime import datetime
from pydantic import Field, AnyHttpUrl
from ninja import Schema
from sensorthings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, EntityId, NestedEntity
from sensorthings.validators import allow_partial

if TYPE_CHECKING:
    from sensorthings.components.things.schemas import Thing
    from sensorthings.components.locations.schemas import Location


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


class HistoricalLocationGetResponse(HistoricalLocationFields, BaseGetResponse):
    thing_link: AnyHttpUrl = Field(None, alias='Thing@iot.navigationLink')
    thing_rel: NestedEntity = Field(None, alias='Thing', nested_class='ThingGetResponse')
    historical_locations_link: AnyHttpUrl = Field(None, alias='HistoricalLocations@iot.navigationLink')
    historical_locations_rel: List[NestedEntity] = Field(
        None,
        alias='HistoricalLocations',
        nested_class='HistoricalLocationsGetResponse'
    )


class HistoricalLocationListResponse(BaseListResponse):
    value: List[HistoricalLocationGetResponse]
