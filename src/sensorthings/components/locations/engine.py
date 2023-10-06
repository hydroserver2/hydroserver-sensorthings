from abc import ABCMeta, abstractmethod
from typing import List


class LocationBaseEngine(metaclass=ABCMeta):

    @abstractmethod
    def get_locations(
            self,
            location_ids: List[str] = None,
            thing_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None
    ) -> (List[dict], int):
        pass

    @abstractmethod
    def create_location(
            self,
            location
    ) -> str:
        pass

    @abstractmethod
    def update_location(
            self,
            location_id: str,
            location
    ) -> None:
        pass

    @abstractmethod
    def delete_location(
            self,
            location_id: str
    ) -> None:
        pass
