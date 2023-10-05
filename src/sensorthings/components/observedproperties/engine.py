from abc import ABCMeta, abstractmethod
from typing import List


class ObservedPropertyEngine(metaclass=ABCMeta):

    @abstractmethod
    def get_observed_properties(
            self,
            observed_property_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None
    ) -> (List[dict], int):
        pass

    @abstractmethod
    def create_observed_property(
            self,
            observed_property
    ) -> str:
        pass

    @abstractmethod
    def update_observed_property(
            self,
            observed_property_id: str,
            observed_property
    ) -> None:
        pass

    @abstractmethod
    def delete_observed_property(
            self,
            observed_property_id: str
    ) -> None:
        pass
