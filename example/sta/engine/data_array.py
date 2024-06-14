from sensorthings.extensions.dataarray.engine import DataArrayBaseEngine
from .utils import SensorThingsUtils


class DataArrayEngine(DataArrayBaseEngine, SensorThingsUtils):
    def create_observations(
            self,
            response,
            entity_body
    ) -> list[int]:

        return []
