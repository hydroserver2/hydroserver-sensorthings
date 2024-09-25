from typing import Optional
from pydantic import Field
from ninja import Schema
from sensorthings.schemas import EntityId
from sensorthings.types import ISOIntervalString


class DeleteObservationsPostBody(Schema):
    """
    Schema for deleting batches of observations from a datastream.

    Attributes
    ----------
    datastream : EntityId
        ID of the Datastream associated whose observations will be deleted.
    phenomenon_time : Optional[ISOIntervalString]
        The range of phenomenon times over which observations will be deleted.
    """

    datastream: EntityId = Field(..., alias='Datastream')
    phenomenon_time: Optional[ISOIntervalString] = Field(None, alias='phenomenonTime')

    class Config:
        populate_by_name = True
