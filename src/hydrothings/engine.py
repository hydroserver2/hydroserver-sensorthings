from abc import ABCMeta, abstractmethod
from pydantic.fields import SHAPE_LIST
from typing import Union
from django.http import HttpRequest
from hydrothings import components as component_schemas
from hydrothings import settings


class SensorThingsAbstractEngine(metaclass=ABCMeta):

    scheme: str
    host: str
    path: str
    version: str
    component: str
    component_path: str

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

    def get_related_components(self):
        """"""

        return {
            name: [
                component for component
                in settings.ST_CAPABILITIES
                if component['SINGULAR_NAME'] == field.type_.__name__
            ][0]['NAME'] if field.shape == SHAPE_LIST
            else field.type_.__name__
            for name, field in getattr(component_schemas, f'{self.component}Relations').__fields__.items()
        }

    def build_related_links(self, response, is_collection=False):
        """"""

        return [
            dict(
                entity,
                **{
                    f'{name}_link': self.get_ref(
                        entity['id'] if is_collection is True else None,
                        related_component
                    ) for name, related_component in self.get_related_components().items()
                }
            ) for entity in response
        ]

    def build_self_links(self, response, is_collection=False):
        """"""

        return [
            dict(
                entity,
                **{
                    'self_link': self.get_ref(entity['id'] if is_collection is True else None)
                }
            ) for entity in response
        ]

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
            entity_id
    ) -> dict:
        """"""

        pass

    @abstractmethod
    def create(
            self,
            entity_body
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
