from abc import ABCMeta, abstractmethod
from typing import Union
from django.http import HttpRequest


class SensorThingsAbstractEngine(metaclass=ABCMeta):

    scheme: str
    host: str
    path: str

    def get_ref(self, entity_id: Union[str, None] = None, related_component: Union[str, None] = None) -> str:
        """
        Builds a reference URL for a given entity.

        :param entity_id: The id of the entity.
        :param related_component: The related component to be appended to the ref URL.
        :return: The entity's reference URL.
        """

        ref_url = f'{self.scheme}://{self.host}{self.path}'

        if entity_id is not None:
            ref_url = f'{ref_url}({entity_id})'

        if related_component is not None:
            ref_url = f'{ref_url}/{related_component}'

        return ref_url

    @abstractmethod
    def list(
            self,
            filters,
            count,
            order_by,
            skip,
            top,
            select,
            expand,
            result_format
    ) -> dict:
        """"""

        pass

    @abstractmethod
    def get(
            self,
            entity_id,
            component=None
    ) -> dict:
        """"""

        pass

    @abstractmethod
    def create(
            self,
            entity_body,
            component=None
    ) -> str:
        """"""

        pass

    @abstractmethod
    def update(
            self,
            entity_id,
            entity_body
    ) -> str:
        """"""

        pass

    @abstractmethod
    def delete(
            self,
            entity_id
    ) -> None:
        """"""

        pass


class SensorThingsRequest(HttpRequest):
    engine: SensorThingsAbstractEngine
