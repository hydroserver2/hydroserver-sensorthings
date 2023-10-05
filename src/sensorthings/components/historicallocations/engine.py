from abc import ABCMeta, abstractmethod
from typing import List


class HistoricalLocationEngine(metaclass=ABCMeta):

    @abstractmethod
    def get_historical_locations(
            self,
            historical_location_ids: List[str] = None,
            thing_ids: List[str] = None,
            location_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None
    ) -> (List[dict], int):
        pass

    @abstractmethod
    def create_historical_location(
            self,
            historical_location
    ) -> str:
        pass

    @abstractmethod
    def update_historical_location(
            self,
            historical_location_id: str,
            historical_location
    ) -> None:
        pass

    @abstractmethod
    def delete_historical_location(
            self,
            historical_location_id: str
    ) -> None:
        pass
