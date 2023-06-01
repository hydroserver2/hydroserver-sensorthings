from typing import TYPE_CHECKING, Literal, List, Union
from pydantic import Field, AnyHttpUrl
from ninja import Schema
from hydrothings.schemas import BaseListResponse, BaseGetResponse, BasePostBody, BasePatchBody, EntityId, \
    NestedEntity
from hydrothings.validators import allow_partial
from hydrothings.extras.iso_types import ISOTime, ISOInterval

if TYPE_CHECKING:
    from hydrothings.components.things.schemas import Thing
    from hydrothings.components.sensors.schemas import Sensor
    from hydrothings.components.observedproperties.schemas import ObservedProperty
    from hydrothings.components.observations.schemas import Observation

observationTypes = Literal[
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CategoryObservation',
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation',
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement',
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation',
    'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_TruthObservation'
]


class UnitOfMeasurement(Schema):
    name: str
    symbol: str
    definition: AnyHttpUrl


# TODO Add validation for temporal duration types.
class DatastreamFields(Schema):
    name: str
    description: str
    unit_of_measurement: UnitOfMeasurement = Field(..., alias='unitOfMeasurement')
    observation_type: observationTypes = Field(..., alias='observationType')
    observed_area: dict = Field({}, alias='observedArea')
    phenomenon_time: Union[ISOTime, ISOInterval, None] = Field(None, alias='phenomenonTime')
    result_time: Union[ISOTime, ISOInterval, None] = Field(None, alias='resultTime')
    properties: dict = {}


class DatastreamRelations(Schema):
    thing: 'Thing'
    sensor: 'Sensor'
    observed_property: 'ObservedProperty'
    observations: List['Observation'] = []


class Datastream(DatastreamFields, DatastreamRelations):
    pass


class DatastreamPostBody(BasePostBody, DatastreamFields):
    thing: Union[EntityId, NestedEntity] = Field(
        ..., alias='Thing', nested_class='ThingPostBody'
    )
    sensor: Union[EntityId, NestedEntity] = Field(
        ..., alias='Sensor', nested_class='SensorPostBody'
    )
    observed_property: Union[EntityId, NestedEntity] = Field(
        ..., alias='ObservedProperty', nested_class='ObservedPropertyPostBody'
    )


@allow_partial
class DatastreamPatchBody(BasePatchBody, DatastreamFields):
    thing: EntityId = Field(..., alias='Thing')
    sensor: EntityId = Field(..., alias='Sensor')
    observed_property: EntityId = Field(..., alias='ObservedProperty')


class DatastreamGetResponse(BaseGetResponse, DatastreamFields):
    thing_link: AnyHttpUrl = Field(None, alias='Thing@iot.navigationLink')
    thing_rel: NestedEntity = Field(None, alias='Thing', nested_class='ThingGetResponse')
    sensor_link: AnyHttpUrl = Field(None, alias='Sensor@iot.navigationLink')
    sensor_rel: NestedEntity = Field(None, alias='Sensor', nested_class='SensorGetResponse')
    observed_property_link: AnyHttpUrl = Field(None, alias='ObservedProperty@iot.navigationLink')
    observed_property_rel: NestedEntity = Field(
        None, alias='ObservedProperty',
        nested_class='ObservedPropertyGetResponse'
    )
    observations_link: AnyHttpUrl = Field(None, alias='Observations@iot.navigationLink')
    observations_rel: List[NestedEntity] = Field(None, alias='Observations', nested_class='ObservationGetResponse')


class DatastreamListResponse(BaseListResponse):
    values: List[DatastreamGetResponse]
