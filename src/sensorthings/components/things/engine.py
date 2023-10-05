from abc import ABCMeta, abstractmethod
from typing import List


class ThingEngine(metaclass=ABCMeta):

    @abstractmethod
    def get_things(
            self,
            thing_ids: List[str] = None,
            location_ids: List[str] = None,
            pagination: dict = None,
            ordering: dict = None,
            filters: dict = None
    ) -> (List[dict], int):
        pass

    @abstractmethod
    def create_thing(
            self,
            thing
    ) -> str:
        pass

    @abstractmethod
    def update_thing(
            self,
            thing_id: str,
            thing
    ) -> None:
        pass

    @abstractmethod
    def delete_thing(
            self,
            thing_id: str
    ) -> None:
        pass
