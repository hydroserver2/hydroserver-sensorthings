from abc import ABCMeta, abstractmethod
from uuid import UUID
from pydantic.fields import SHAPE_LIST
from typing import Union, Tuple, List
from django.http import HttpRequest
from hydrothings import components as component_schemas
from hydrothings import settings


class SensorThingsAbstractEngine(metaclass=ABCMeta):
    """

    """

    scheme: str
    host: str
    path: str
    version: str
    component: str
    component_path: str

    def get_ref(self, entity_id: Union[str, None] = None, related_component: Union[str, None] = None) -> str:
        """
        Builds a reference URL for a given entity.

        Parameters
        ----------
        entity_id : str
            The ID of the entity.
        related_component : str
            The related component to be appended to the ref URL.

        Returns
        -------
        str
            The entity's reference URL.
        """

        ref_url = f'{self.scheme}://{self.host}{self.path}'

        if entity_id is not None:
            ref_url = f'{ref_url}({entity_id})'

        if related_component is not None:
            ref_url = f'{ref_url}/{related_component}'

        return ref_url

    def get_related_components(self) -> dict:
        """
        Get all components related to this component.

        Returns
        -------
        dict
            The component's related components.
        """

        return {
            name: [
                component for component
                in settings.ST_CAPABILITIES
                if component['SINGULAR_NAME'] == field.type_.__name__
            ][0]['NAME'] if field.shape == SHAPE_LIST
            else field.type_.__name__
            for name, field in getattr(component_schemas, f'{self.component}Relations').__fields__.items()
        }

    def build_related_links(self, entity: dict, is_collection: bool = False) -> dict:
        """
        Creates SensorThings links to related components.

        Parameters
        ----------
        entity : dict
            The entity response object dictionary.
        is_collection : bool
            Includes the entity ID in the reference URL if True, and omits it if False.

        Returns
        -------
        dict
            The entity response object dictionary with related links included.
        """

        return dict(
            entity,
            **{
                f'{name}_link': self.get_ref(
                    entity['id'] if is_collection is True else None,
                    related_component
                ) for name, related_component in self.get_related_components().items()
            }
        )

    def build_self_links(self, entity: dict, is_collection: bool = False) -> dict:
        """
        Creates SensorThings self-referential link.

        Parameters
        ----------
        entity : dict
            The entity response object dictionary.
        is_collection : bool
            Includes the entity ID in the reference URL if True, and omits it if False.

        Returns
        -------
        dict
            The entity response object dictionary with the self link included.
        """

        return dict(
            entity,
            **{
                'self_link': self.get_ref(entity['id'] if is_collection is True else None)
            }
        )

    @abstractmethod
    def resolve_entity_id_chain(self, entity_chain: List[Tuple[str, Union[UUID, int, str]]]) -> bool:
        """
        Abstract method for resolving an entity chain passed to the API.

        SensorThings supports nested references to entities in URL paths. The Django HydroThings middleware will check
        the nested components to ensure each one is related to its parent and build a list of IDs that need to be
        verified by this method.

        Parameters
        ----------
        entity_chain : list
            A list of tuples representing the entity chain where the first object in the tuple is a string representing
            the component name, and the second object in the tuple is a string, int, or UUID representing the entity ID.

        Returns
        -------
        bool
            Returns True if the entity chain could be fully resolved, and False if any part of the entity chain could
            not be found or resolved.
        """

        pass

    @abstractmethod
    def list(
            self,
            filters,
            count,
            order_by,
            skip,
            top,
            select,
            expand
    ) -> dict:
        """
        Abstract method for handling GET collection requests.

        This method should return a dictionary representing a collection of entities for this component and apply all
        the given query parameters.

        Parameters
        ----------
        filters

        count : bool
            If True, the pre-pagination result count should be included in the response. If False, the count should be
            omitted.
        order_by

        skip : int
            An integer representing the number of records to skip in the response.
        top : int
            An integer representing the number of records the response should be limited to.
        select
            Represents a subset of this component's fields to include in the response.
        expand
            Represents related components whose fields should be included in the response.

        Returns
        -------
        dict
            A dictionary object representing the SensorThings GET collection response.
        """

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
            entity_body,
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
    entity_chain: Tuple[str, Union[UUID, int, str]]
