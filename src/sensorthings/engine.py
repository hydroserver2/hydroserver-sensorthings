from abc import ABCMeta, abstractmethod
from uuid import UUID
from pydantic.fields import SHAPE_LIST
from typing import Union, Tuple, List, Optional
from django.http import HttpRequest
from sensorthings import components as component_schemas
from sensorthings import settings
from sensorthings.schemas import BasePostBody, BasePatchBody
from sensorthings.utils import lookup_component


class SensorThingsAbstractEngine(metaclass=ABCMeta):
    """
    Abstract base class for a SensorThings engine.

    A SensorThings API must be linked to a SensorThings engine to perform database operations. This class defines all
    required methods for an engine class and should be inherited by any SensorThings engine used by an API.
    """

    scheme: str
    host: str
    path: str
    version: str
    component: str
    component_path: str

    def get_ref(
            self,
            entity_id: Union[str, None] = None,
            related_component: Union[str, None] = None,
            override_component: Union[str, None] = None
    ) -> str:
        """
        Builds a reference URL for a given entity.

        Parameters
        ----------
        entity_id : str
            The ID of the entity.
        related_component : str
            The related component to be appended to the ref URL.
        override_component : str
            A value used to override the base component in the URL.

        Returns
        -------
        str
            The entity's reference URL.
        """

        if override_component is not None:
            override_component = '/' + lookup_component(override_component, 'camel_singular', 'camel_plural')

        ref_url = f'{self.scheme}://{self.host}{override_component if override_component is not None else self.path}'

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

    def build_next_link(self, top: int, skip: int) -> str:
        """
        Creates SensorThings next link for paginated responses.

        Parameters
        ----------
        top : int
            An integer representing how many records are returned in the response.
        skip : int
            An integer representing how many records are skipped in the response.

        Returns
        -------
        str
            A URL that links to the next dataset following the subset of data in the current response.
        """

        return f'{self.get_ref()}?$top={top}&$skip={top+skip}'

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
            entity_id: str,
            expand
    ) -> Optional[dict]:
        """
        Abstract method for handling GET entity requests.

        This method should return a dictionary representing an entity with the given entity ID.

        Parameters
        ----------
        entity_id : str
            The ID of the entity to be returned.
        expand
            Represents related components whose fields should be included in the response.

        Returns
        -------
        dict
            A dictionary object representing the SensorThings GET entity response.
        """

        pass

    @abstractmethod
    def create(
            self,
            entity_body: BasePostBody,
    ) -> str:
        """
        Abstract method for handling POST entity requests.

        This method should create a new entity and return the ID of the created entity.

        Parameters
        ----------
        entity_body : BasePostBody
            A dictionary object containing the attributes of the entity that will be created.

        Returns
        -------
        str
            The ID of the newly created entity.
        """

        pass

    @abstractmethod
    def update(
            self,
            entity_id: str,
            entity_body: BasePatchBody
    ) -> str:
        """
        Abstract method for handling PATCH entity requests.

        This method should update an existing entity with the attributes included in the entity_body and return the ID
        of the updated entity.

        Parameters
        ----------
        entity_id : str
            The ID of the entity to be updated.
        entity_body : BasePatchBody
            A dictionary object containing the attributes of the entity that will be updated.

        Returns
        -------
        str
            The ID of the updated entity.
        """

        pass

    @abstractmethod
    def delete(
            self,
            entity_id
    ) -> None:
        """
        Abstract method for handling DELETE entity requests.

        This method should delete an existing entity with the given entity_id.

        Parameters
        ----------
        entity_id : str
            The ID of the entity t obe deleted.

        Returns
        -------
        None
        """

        pass


class SensorThingsRequest(HttpRequest):
    """
    The SensorThings request class.

    This class extends Django's HttpRequest class to include an engine class, component name, component path, and an
    entity_chain tuple. These attributes should be added to the request in the SensorThings middleware before calling a
    view function.
    """

    engine: SensorThingsAbstractEngine
    auth: str
    component: str
    component_path: List[str]
    entity_chain: List[Tuple[str, Union[UUID, int, str]]]
