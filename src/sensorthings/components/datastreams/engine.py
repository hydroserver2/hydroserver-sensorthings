from abc import ABCMeta, abstractmethod
from typing import List


class DatastreamBaseEngine(metaclass=ABCMeta):

    @abstractmethod
    def get_datastreams(
            self,
            datastream_ids: List[str] = None,
            observed_property_ids: List[str] = None,
            sensor_ids: List[str] = None,
            thing_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None
    ) -> (List[dict], int):
        pass

    @abstractmethod
    def create_datastream(
            self,
            datastream
    ) -> str:
        pass

    @abstractmethod
    def update_datastream(
            self,
            datastream_id: str,
            datastream
    ) -> None:
        pass

    @abstractmethod
    def delete_datastream(
            self,
            datastream_id: str
    ) -> None:
        pass
