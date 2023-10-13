from abc import ABCMeta, abstractmethod
from typing import List


class ObservationBaseEngine(metaclass=ABCMeta):

    @abstractmethod
    def get_observations(
            self,
            observation_ids: List[str] = None,
            datastream_ids: List[str] = None,
            feature_of_interest_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None,
            expanded: bool = False
    ) -> (List[dict], int):
        pass

    @abstractmethod
    def create_observation(
            self,
            observation
    ) -> str:
        pass

    @abstractmethod
    def create_observation_bulk(
            self,
            observations
    ) -> List[str]:
        pass

    @abstractmethod
    def update_observation(
            self,
            observation_id: str,
            observation
    ) -> None:
        pass

    @abstractmethod
    def delete_observation(
            self,
            observation_id: str
    ) -> None:
        pass


