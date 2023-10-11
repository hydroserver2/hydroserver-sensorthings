from typing import TYPE_CHECKING, Literal, List
from pydantic import Field, AnyHttpUrl, validator
from ninja import Schema
from sensorthings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, NestedEntity
from sensorthings.validators import allow_partial
from sensorthings.components.sensors.utils import metadata_validator

if TYPE_CHECKING:
    from sensorthings.components.datastreams.schemas import Datastream


sensorEncodingTypes = Literal[
    'application/pdf',
    'http://www.opengis.net/doc/IS/SensorML/2.0',
    'text/html'
]


class SensorFields(Schema):
    name: str
    description: str
    encoding_type: sensorEncodingTypes = Field(..., alias='encodingType')
    sensor_metadata: str = Field(..., alias='metadata')
    properties: dict = {}

    _metadata_validator = validator('sensor_metadata', allow_reuse=True, check_fields=False)(metadata_validator)


class SensorRelations(Schema):
    datastreams: List['Datastream'] = []


class Sensor(SensorFields, SensorRelations):
    pass


class SensorPostBody(BasePostBody, SensorFields):
    datastreams: List[NestedEntity] = Field(
        [], alias='Datastreams', nested_class='DatastreamPostBody'
    )


@allow_partial
class SensorPatchBody(BasePatchBody, SensorFields):
    pass


class SensorGetResponse(SensorFields, BaseGetResponse):
    datastreams_link: AnyHttpUrl = Field(None, alias='Datastreams@iot.navigationLink')
    datastreams_rel: List[NestedEntity] = Field(None, alias='Datastreams', nested_class='DatastreamGetResponse')


class SensorListResponse(BaseListResponse):
    value: List[SensorGetResponse]
