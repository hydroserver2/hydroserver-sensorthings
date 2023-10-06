from abc import ABCMeta, abstractmethod
from typing import List


class FeatureOfInterestBaseEngine(metaclass=ABCMeta):

    @abstractmethod
    def get_features_of_interest(
            self,
            feature_of_interest_ids: List[str] = None,
            observation_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None
    ) -> (List[dict], int):
        pass

    @abstractmethod
    def create_feature_of_interest(
            self,
            feature_of_interest
    ) -> str:
        pass

    @abstractmethod
    def update_feature_of_interest(
            self,
            feature_of_interest_id: str,
            feature_of_interest
    ) -> None:
        pass

    @abstractmethod
    def delete_feature_of_interest(
            self,
            feature_of_interest_id: str
    ) -> None:
        pass
