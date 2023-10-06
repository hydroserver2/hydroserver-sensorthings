from abc import ABCMeta, abstractmethod
from typing import List


class SensorBaseEngine(metaclass=ABCMeta):

    @abstractmethod
    def get_sensors(
            self,
            sensor_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None
    ) -> (List[dict], int):
        pass

    @abstractmethod
    def create_sensor(
            self,
            sensor
    ) -> str:
        pass

    @abstractmethod
    def update_sensor(
            self,
            sensor_id: str,
            sensor
    ) -> None:
        pass

    @abstractmethod
    def delete_sensor(
            self,
            sensor_id: str
    ) -> None:
        pass
