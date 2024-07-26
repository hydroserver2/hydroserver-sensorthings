from typing import TYPE_CHECKING, Union, List, Optional
from pydantic import Field
from ninja import Schema
from sensorthings.schemas import BaseComponent, BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, \
    EntityId
from sensorthings.types import AnyHttpUrlString

if TYPE_CHECKING:
    from sensorthings.components.locations.schemas import Location
    from sensorthings.components.historicallocations.schemas import HistoricalLocation
    from sensorthings.components.datastreams.schemas import Datastream


class ThingFields(Schema):
    """
    A schema representing the fields of a thing.

    Attributes
    ----------
    name : str
        The name of the thing.
    description : str
        The description of the thing.
    properties : Optional[dict], optional
        Additional properties of the thing.
    """

    name: str = Field(..., alias='name')
    description: str = Field(..., alias='description')
    properties: Optional[dict] = Field(None, alias='properties')

    class Config:
        populate_by_name = True


class ThingRelations(Schema):
    """
    A schema representing the relations of a thing to other components.

    Attributes
    ----------
    locations : List['Location']
        The locations associated with the thing.
    historical_locations : List['HistoricalLocation']
        The historical locations associated with the thing.
    datastreams : List['Datastream']
        The datastreams associated with the thing.
    """

    locations: List['Location'] = Field([], alias='Locations', relationship='many_to_many', back_ref='thing_id')
    historical_locations: List['HistoricalLocation'] = Field(
        [], alias='HistoricalLocations', relationship='one_to_many', back_ref='thing_id'
    )
    datastreams: List['Datastream'] = Field([], alias='Datastreams', relationship='one_to_many', back_ref='thing_id')


class Thing(BaseComponent, ThingFields, ThingRelations):
    """
    A schema representing a thing.

    This class combines the fields and relations of a thing, and extends the BaseComponent class.
    """

    class Config:
        json_schema_extra = {
            'name_ref': ('Things', 'thing', 'things')
        }


class ThingPostBody(BasePostBody, ThingFields):
    """
    A schema for the body of a POST request to create a new thing.

    Attributes
    ----------
    locations : List[Union[EntityId]]
        The IDs of the locations associated with the thing.
    historical_locations : List[EntityId]
        The IDs of the historical locations associated with the thing.
    datastreams : List[EntityId]
        The IDs of the datastreams associated with the thing.
    """

    locations: List[Union[EntityId]] = Field(
        [], alias='Locations', nested_class='LocationPostBody'
    )
    historical_locations: List[EntityId] = Field(
        [], alias='HistoricalLocations', nested_class='HistoricalLocationPostBody'
    )
    datastreams: List[EntityId] = Field(
        [], alias='Datastreams', nested_class='DatastreamPostBody'
    )


class ThingPatchBody(BasePatchBody, ThingFields):
    """
    A schema for the body of a PATCH request to update an existing thing.

    Attributes
    ----------
    locations : Optional[List[EntityId]]
        The IDs of the locations associated with the thing.
    """

    locations: Optional[List[EntityId]] = Field([], alias='Locations')


class ThingGetResponse(ThingFields, BaseGetResponse):
    """
    A schema for the response of a GET request for a thing.

    Attributes
    ----------
    locations_link : AnyHttpUrlString
        The navigation link for the locations associated with the thing.
    locations_rel : List[dict]
        The relationship details for the locations associated with the thing.
    historical_locations_link : AnyHttpUrlString
        The navigation link for the historical locations associated with the thing.
    historical_locations_rel : List[dict]
        The relationship details for the historical locations associated with the thing.
    datastreams_link : AnyHttpUrlString
        The navigation link for the datastreams associated with the thing.
    datastreams_rel : List[dict]
        The relationship details for the datastreams associated with the thing.
    """

    locations_link: AnyHttpUrlString = Field(None, alias='Locations@iot.navigationLink')
    locations_rel: List[dict] = Field(None, alias='Locations', nested_class='LocationGetResponse')
    historical_locations_link: AnyHttpUrlString = Field(None, alias='HistoricalLocations@iot.navigationLink')
    historical_locations_rel: List[dict] = Field(
        None,
        alias='HistoricalLocations',
        nested_class='HistoricalLocationGetResponse'
    )
    datastreams_link: AnyHttpUrlString = Field(None, alias='Datastreams@iot.navigationLink')
    datastreams_rel: List[dict] = Field(None, alias='Datastreams', nested_class='DatastreamGetResponse')


class ThingListResponse(BaseListResponse):
    """
    A schema for the response of a GET request for a list of things.

    Attributes
    ----------
    value : List[ThingGetResponse]
        The list of things in the response.
    """

    value: List[ThingGetResponse]
