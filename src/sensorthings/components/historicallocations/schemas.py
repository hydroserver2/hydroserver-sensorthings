from typing import TYPE_CHECKING, List, Union, Dict, Optional
from datetime import datetime
from pydantic import Field
from ninja import Schema
from sensorthings.schemas import (BaseComponent, BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody,
                                  EntityId)
from sensorthings.types import AnyHttpUrlString

if TYPE_CHECKING:
    from sensorthings.components.things.schemas import Thing
    from sensorthings.components.locations.schemas import Location


class HistoricalLocationFields(Schema):
    """
    A schema representing the fields of a historical location.

    Attributes
    ----------
    time : datetime
        The time at which the historical location is recorded.
    """

    time: datetime = Field(..., alias='time')


class HistoricalLocationRelations(Schema):
    """
    A schema representing the relations of a historical location to other components.

    Attributes
    ----------
    thing : 'Thing'
        The thing associated with the historical location.
    locations : List['Location']
        The list of locations associated with the historical location.
    """

    thing: 'Thing' = Field(..., alias='Thing', relationship='many_to_one', back_ref='thing_id')
    locations: List['Location'] = Field(
        ..., alias='Locations', relationship='many_to_many', back_ref='historical_location_id'
    )


class HistoricalLocation(BaseComponent, HistoricalLocationFields, HistoricalLocationRelations):
    """
    A schema representing a historical location.

    This class combines the fields and relations of a historical location, and extends the BaseComponent class.
    """

    class Config:
        json_schema_extra = {
            'name_ref': ('HistoricalLocations', 'historical_location', 'historical_locations'),
        }


class HistoricalLocationPostBody(BasePostBody, HistoricalLocationFields):
    """
    A schema for the body of a POST request to create a new historical location.

    Attributes
    ----------
    thing : Union[EntityId]
        The thing associated with the historical location.
    locations : List[Union[EntityId]]
        The list of location IDs associated with the historical location.
    """

    thing: Union[EntityId] = Field(
        ..., alias='Thing', nested_class='ThingPostBody'
    )
    locations: List[Union[EntityId]] = Field(
        ..., alias='Locations', nested_class='LocationPostBody'
    )


class HistoricalLocationPatchBody(HistoricalLocationFields, BasePatchBody):
    """
    A schema for the body of a PATCH request to update an existing historical location.

    Attributes
    ----------
    thing : Optional[EntityId]
        The thing associated with the historical location.
    locations : Optional[List[EntityId]]
        The list of location IDs associated with the historical location.
    """

    thing: Optional[EntityId] = Field(None, alias='Thing')
    locations: Optional[List[EntityId]] = Field(None, alias='Locations')


class HistoricalLocationGetResponse(HistoricalLocationFields, BaseGetResponse):
    """
    A schema for the response of a GET request for a historical location.

    Attributes
    ----------
    thing_link : AnyHttpUrlString, optional
        The navigation link for the thing associated with the historical location.
    thing_rel : Dict, optional
        The relationship details for the thing associated with the historical location.
    historical_locations_link : AnyHttpUrlString, optional
        The navigation link for the historical locations.
    historical_locations_rel : List[dict], optional
        The relationship details for the historical locations.
    """

    thing_link: AnyHttpUrlString = Field(None, alias='Thing@iot.navigationLink')
    thing_rel: Dict = Field(None, alias='Thing', nested_class='ThingGetResponse')
    historical_locations_link: AnyHttpUrlString = Field(None, alias='HistoricalLocations@iot.navigationLink')
    historical_locations_rel: List[dict] = Field(
        None,
        alias='HistoricalLocations',
        nested_class='HistoricalLocationsGetResponse'
    )


class HistoricalLocationListResponse(BaseListResponse):
    """
    A schema for the response of a GET request for a list of historical locations.

    Attributes
    ----------
    value : List[HistoricalLocationGetResponse]
        The list of historical locations.
    """

    value: List[HistoricalLocationGetResponse]
