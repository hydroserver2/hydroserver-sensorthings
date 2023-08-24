from .datastreams.schemas import *
from .featuresofinterest.schemas import *
from .historicallocations.schemas import *
from .locations.schemas import *
from .observations.schemas import *
from .observedproperties.schemas import *
from .root.schemas import *
from .sensors.schemas import *
from .things.schemas import *


DatastreamRelations.update_forward_refs(
    Thing=Thing,
    Sensor=Sensor,
    ObservedProperty=ObservedProperty,
    Observation=Observation
)

FeatureOfInterestRelations.update_forward_refs(
    Observation=Observation
)

HistoricalLocationRelations.update_forward_refs(
    Thing=Thing,
    Location=Location
)

LocationRelations.update_forward_refs(
    Thing=Thing,
    HistoricalLocation=HistoricalLocation
)

ObservationRelations.update_forward_refs(
    FeatureOfInterest=FeatureOfInterest,
    Datastream=Datastream
)

ObservedPropertyRelations.update_forward_refs(
    Datastream=Datastream
)

SensorRelations.update_forward_refs(
    Datastream=Datastream
)

ThingRelations.update_forward_refs(
    Datastream=Datastream,
    Location=Location,
    HistoricalLocation=HistoricalLocation
)
