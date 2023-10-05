from typing import TYPE_CHECKING, Literal, List, Union
from pydantic import Field, AnyHttpUrl
from geojson_pydantic import Feature
from ninja import Schema
from sensorthings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, EntityId, NestedEntity
from sensorthings.validators import allow_partial

if TYPE_CHECKING:
    from sensorthings.components.things.schemas import Thing
    from sensorthings.components.historicallocations.schemas import HistoricalLocation


locationEncodingTypes = Literal['application/geo+json']


class LocationFields(Schema):
    name: str
    description: str
    encoding_type: locationEncodingTypes = Field(..., alias='encodingType')
    location: Feature
    properties: dict = {}


class LocationRelations(Schema):
    things: List['Thing'] = []
    historical_locations: List['HistoricalLocation'] = []


class Location(LocationFields, LocationRelations):
    pass


class LocationPostBody(BasePostBody, LocationFields):
    things: List[Union[EntityId, NestedEntity]] = Field(
        [], alias='Things', nested_class='ThingPostBody'
    )
    historical_locations: List[Union[EntityId, NestedEntity]] = Field(
        [], alias='HistoricalLocations', nested_class='HistoricalLocationPostBody'
    )


@allow_partial
class LocationPatchBody(LocationFields, BasePatchBody):
    things: List[EntityId] = Field([], alias='Things')
    historical_locations: List[EntityId] = Field([], alias='HistoricalLocations')


class LocationGetResponse(LocationFields, BaseGetResponse):
    things_link: AnyHttpUrl = Field(None, alias='Things@iot.navigationLink')
    things_rel: List[NestedEntity] = Field(None, alias='Things', nested_class='ThingGetResponse')
    historical_locations_link: AnyHttpUrl = Field(None, alias='HistoricalLocations@iot.navigationLink')
    historical_locations_rel: List[NestedEntity] = Field(
        None,
        alias='HistoricalLocations',
        nested_class='HistoricalLocationGetResponse'
    )


class LocationListResponse(BaseListResponse):
    values: List[LocationGetResponse]
