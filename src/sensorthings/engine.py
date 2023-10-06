import re
from abc import ABCMeta
from uuid import UUID
from typing import Union, Tuple, List, Optional
from ninja.errors import HttpError
from django.http import HttpRequest
from django.urls.exceptions import Http404
from odata_query.grammar import ODataParser, ODataLexer
from odata_query.exceptions import ParsingException
from sensorthings import components as component_schemas
from sensorthings import settings
from sensorthings.utils import lookup_component
from sensorthings.schemas import ListQueryParams
from sensorthings.components.things.engine import ThingBaseEngine
from sensorthings.components.locations.engine import LocationBaseEngine
from sensorthings.components.historicallocations.engine import HistoricalLocationBaseEngine
from sensorthings.components.datastreams.engine import DatastreamBaseEngine
from sensorthings.components.sensors.engine import SensorBaseEngine
from sensorthings.components.observedproperties.engine import ObservedPropertyBaseEngine
from sensorthings.components.featuresofinterest.engine import FeatureOfInterestBaseEngine
from sensorthings.components.observations.engine import ObservationBaseEngine


class SensorThingsBaseEngine(
    ThingBaseEngine,
    LocationBaseEngine,
    HistoricalLocationBaseEngine,
    DatastreamBaseEngine,
    SensorBaseEngine,
    ObservedPropertyBaseEngine,
    FeatureOfInterestBaseEngine,
    ObservationBaseEngine,
    metaclass=ABCMeta
):
    """
    Abstract base class for a SensorThings engine.

    A SensorThings API must be linked to a SensorThings engine to perform database operations. This class defines all
    required methods for an engine class and should be inherited by any SensorThings engine used by an API.
    """

    def __init__(
            self,
            host,
            scheme,
            path,
            version,
            component
    ):
        self.host = host
        self.scheme = scheme
        self.path = path
        self.version = version
        self.component = component

    def list_entities(self, request, query_params, component=None, join_ids=None, drop_related_links=False):
        """"""

        if not join_ids:
            join_ids = {}

        entities, count = getattr(self, 'get_' + lookup_component(
            component if component else self.component, 'camel_singular', 'snake_plural'
        ))(
            filters=self.get_filters(query_params.get('filters')) if query_params.get('filters') else None,
            pagination=self.get_pagination(query_params),
            ordering=query_params.get('order_by'),
            **join_ids
        )

        next_link = self.build_next_link(
            skip=query_params.get('skip'),
            top=query_params.get('top'),
            count=count
        )

        entities = self.build_links_and_nested_components(
            request=request,
            component=component if component else self.component,
            values=entities,
            expand=query_params.get('expand'),
            drop_related_links=drop_related_links
        )

        return {
            'count': count if query_params.get('count') is True else None,
            'values': entities,
            'next_link': next_link
        }

    def get_entity(self, request, entity_id, query_params):

        entities, count = getattr(self, 'get_' + lookup_component(
            self.component, 'camel_singular', 'snake_plural'
        ))(
            filters=self.get_filters(f"id eq '{entity_id}'"),
        )

        entities = self.build_links_and_nested_components(
            request=request,
            component=self.component,
            values=entities,
            expand=query_params.get('expand')
        )

        entity = next(iter(entities), None)

        if not entity:
            raise HttpError(404, 'Record not found.')

        return entity

    def create_entity(self, request, entity_body):
        pass

    def update_entity(self, request, entity_id, entity_body):
        pass

    def delete_entity(self, request, entity_id):
        pass

    def get_ref(
            self,
            component: Optional[str] = None,
            entity_id: Optional[str] = None,
            related_component: Optional[str] = None,
            is_collection: Optional[bool] = False
    ) -> str:
        """
        Builds a reference URL for a given entity.

        Parameters
        ----------
        component : str
            The value to use as the base component in the URL.
        entity_id : str
            The ID of the entity if there is one.
        related_component : str
            The related component to be appended to the ref URL.
        is_collection : bool
            Sets whether the related component is a collection or not.

        Returns
        -------
        str
            The entity's reference URL.
        """

        base_url = getattr(settings, 'PROXY_BASE_URL', f'{self.scheme}://{self.host}') + \
            f'/{settings.ST_API_PREFIX}/v{self.version}'

        ref_url = f'{base_url}/{component if component else self.component}'

        if entity_id is not None:
            ref_url = f'{ref_url}({entity_id})'

        if related_component is not None:
            if is_collection is True:
                related_component = lookup_component(related_component, 'camel_singular', 'camel_plural')
            ref_url = f'{ref_url}/{related_component}'

        return ref_url

    def resolve_nested_resource_path(self, nested_resources):
        """"""

        entity = None
        replacement_id = None
        filter_id_string = None
        for nested_resource in nested_resources:
            if nested_resource[1] is not None:
                component = lookup_component(nested_resource[0], 'camel_singular', 'snake_singular')
                if nested_resource[1] != 'temp_id':
                    lookup_id = nested_resource[1]
                else:
                    lookup_id = entity[f'{component}_id']
                    replacement_id = lookup_id

                entity = next(iter(getattr(
                    self, f'get_{lookup_component(component, "snake_singular", "snake_plural")}'
                )(
                    **{f'{component}_ids': [lookup_id]}
                )[0]), None)

                if not entity:
                    raise Http404

                filter_id_string = f'{nested_resource[0]}/id eq {lookup_id}'

            else:
                filter_id_string = None

        return replacement_id, filter_id_string

    @staticmethod
    def get_filters(filter_string: str):

        lexer = ODataLexer()
        parser = ODataParser()

        try:
            return parser.parse(lexer.tokenize(filter_string))
        except ParsingException:
            raise HttpError(422, 'Failed to parse filter parameter.')

    @staticmethod
    def get_pagination(query_params):
        """"""

        return {
            'skip': query_params['skip'] if query_params['skip'] is not None else 0,
            'top': query_params['top'] if query_params['top'] is not None else 100,
            'count': query_params['count'] if query_params['count'] is not None else False
        }

    def build_next_link(self, count: int, top: Optional[int] = None, skip: Optional[int] = None):
        """"""

        if top is None:
            top = 100

        if skip is None:
            skip = 0

        if count is not None and top + skip < count:
            return f'{self.get_ref()}?$top={top}&$skip={top + skip}'
        else:
            return None

    def build_links_and_nested_components(self, request, component, values, expand, drop_related_links=False):
        """"""

        related_components = self.get_related_components(component)
        expand_properties = self.parse_expand_parameter(component, expand)

        for value in values:

            value['self_link'] = self.get_ref(
                component=component,
                entity_id=value['id']
            )

            for related_component, component_meta in related_components.items():
                if related_component not in expand_properties:
                    value[f'{related_component}_link'] = self.get_ref(
                        component=component,
                        entity_id=value['id'],
                        related_component=component_meta['component'],
                        is_collection=component_meta['is_collection']
                    ) if not drop_related_links else None
                else:
                    expand_properties[related_component]['join_ids'].append(
                        value[expand_properties[related_component]['join_field']]
                    )

        for expand_property_name, expand_property_meta in expand_properties.items():
            if len(expand_property_meta['join_ids']) > 0:
                if expand_property_meta['join_field'] == 'id':
                    join_field = lookup_component(
                        component, 'camel_singular', 'snake_singular'
                    ) + '_ids'
                else:
                    join_field = expand_property_meta['join_field'] + 's'
                related_entities = {
                    entity.get('id'): entity for entity in self.list_entities(
                        request=request,
                        query_params=expand_property_meta['query_params'],
                        component=expand_property_meta['component'],
                        join_ids={
                            join_field: expand_property_meta['join_ids']
                        },
                        drop_related_links=True
                    ).get('values')
                }

                for value in values:
                    if related_components[expand_property_name]['is_many_to_many']:
                        value[f'{expand_property_name}_rel'] = [
                            getattr(
                                component_schemas, f'{expand_property_meta["component"]}GetResponse'
                            )(**related_entity).dict(
                                by_alias=True,
                                exclude_none=True
                            ) for related_entity in related_entities.values()
                            if value['id'] in related_entity[join_field]
                        ]
                    elif related_components[expand_property_name]['is_collection']:
                        value[f'{expand_property_name}_rel'] = [
                            getattr(
                                component_schemas, f'{expand_property_meta["component"]}GetResponse'
                            )(**related_entity).dict(
                                by_alias=True,
                                exclude_none=True
                            ) for related_entity in related_entities.values()
                            if related_entity[join_field[:-1]] == value['id']
                        ]
                    else:
                        value[f'{expand_property_name}_rel'] = getattr(
                            component_schemas, f'{expand_property_meta["component"]}GetResponse'
                        )(**related_entities[
                            value[expand_property_meta['join_field']]
                        ]).dict(
                            by_alias=True,
                            exclude_none=True
                        )

        return values

    @staticmethod
    def get_related_components(component):
        """
        Get all components related to this component.

        Returns
        -------
        dict
            The component's related components.
        """

        many_to_many_relations = {
            'Thing': ['Location'],
            'Location': ['Thing', 'HistoricalLocation'],
            'HistoricalLocation': ['Location']
        }

        return {
            name: {
                'component': field.type_.__name__,
                'is_collection': True if lookup_component(name, 'snake_singular', 'camel_singular') is None else False,
                'is_many_to_many': True if field.type_.__name__ in many_to_many_relations.get(component, []) else False
            } for name, field in getattr(component_schemas, f'{component}Relations').__fields__.items()
        }

    def parse_expand_parameter(self, component, expand_parameter):
        """"""

        if not expand_parameter:
            expand_parameter = ''
        expand_properties = {}
        expand_components = expand_parameter.split(',')
        related_components = self.get_related_components(component)

        for expand_component in expand_components:
            component_name = re.sub(r'(?<!^)(?=[A-Z])', '_', expand_component.split('/')[0].split('(')[0]).lower()
            if component_name not in related_components:
                continue

            nested_query_params = re.search(r'\(.*?\)', expand_component.split('/')[0])
            nested_query_params = nested_query_params.group(0)[1:-1] if nested_query_params else ''
            nested_query_params = {
                nested_query_param.split('=')[0]: nested_query_param.split('=')[1]
                for nested_query_param in nested_query_params.split('&') if nested_query_param
            }

            if component_name not in expand_properties:
                expand_properties[component_name] = {
                    'component': related_components[component_name]['component'],
                    'join_field': 'id' if related_components[component_name]['is_collection'] else
                    lookup_component(
                        related_components[component_name]['component'], 'camel_singular', 'snake_singular'
                    ) + '_id',
                    'join_ids': [],
                    'query_params': nested_query_params
                }

            if len(expand_component.split('/')) > 1:
                expand_properties[component_name]['query_params']['$expand'] = ','.join(
                    (
                        *expand_properties[component_name]['query_params']['$expand'].split(','),
                        expand_component.split('/')[1],
                    )
                ) if '$expand' in expand_properties[component_name]['query_params'] else expand_component.split('/')[1]

        for expand_property in expand_properties.values():
            expand_property['query_params'] = ListQueryParams(**expand_property['query_params']).dict()

        return expand_properties





#     def get_related_components(self) -> dict:
#         """
#         Get all components related to this component.
#
#         Returns
#         -------
#         dict
#             The component's related components.
#         """
#
#         return {
#             name: [
#                 component for component
#                 in settings.ST_CAPABILITIES
#                 if component['SINGULAR_NAME'] == field.type_.__name__
#             ][0]['NAME'] if field.shape == SHAPE_LIST
#             else field.type_.__name__
#             for name, field in getattr(component_schemas, f'{self.component}Relations').__fields__.items()
#         }










# class SensorThingsAbstractEngine(metaclass=ABCMeta):
#     """
#     Abstract base class for a SensorThings engine.
#
#     A SensorThings API must be linked to a SensorThings engine to perform database operations. This class defines all
#     required methods for an engine class and should be inherited by any SensorThings engine used by an API.
#     """
#
#     scheme: str
#     host: str
#     path: str
#     version: str
#     component: str
#     component_path: str
#
#     def get_ref(
#             self,
#             entity_id: Union[str, None] = None,
#             related_component: Union[str, None] = None,
#             override_component: Union[str, None] = None
#     ) -> str:
#         """
#         Builds a reference URL for a given entity.
#
#         Parameters
#         ----------
#         entity_id : str
#             The ID of the entity.
#         related_component : str
#             The related component to be appended to the ref URL.
#         override_component : str
#             A value used to override the base component in the URL.
#
#         Returns
#         -------
#         str
#             The entity's reference URL.
#         """
#
#         if override_component is not None:
#             override_component = '/' + lookup_component(override_component, 'camel_singular', 'camel_plural')
#
#         base_url = getattr(settings, 'PROXY_BASE_URL', f'{self.scheme}://{self.host}') + \
#             f'/{settings.ST_API_PREFIX}/v{self.version}'
#
#         ref_url = f'{base_url}{override_component if override_component else "/" + self.path}'
#
#         if entity_id is not None:
#             ref_url = f'{ref_url}({entity_id})'
#
#         if related_component is not None:
#             ref_url = f'{ref_url}/{related_component}'
#
#         return ref_url
#
#     def get_related_components(self) -> dict:
#         """
#         Get all components related to this component.
#
#         Returns
#         -------
#         dict
#             The component's related components.
#         """
#
#         return {
#             name: [
#                 component for component
#                 in settings.ST_CAPABILITIES
#                 if component['SINGULAR_NAME'] == field.type_.__name__
#             ][0]['NAME'] if field.shape == SHAPE_LIST
#             else field.type_.__name__
#             for name, field in getattr(component_schemas, f'{self.component}Relations').__fields__.items()
#         }
#
#     def build_related_links(self, entity: dict, is_collection: bool = False) -> dict:
#         """
#         Creates SensorThings links to related components.
#
#         Parameters
#         ----------
#         entity : dict
#             The entity response object dictionary.
#         is_collection : bool
#             Includes the entity ID in the reference URL if True, and omits it if False.
#
#         Returns
#         -------
#         dict
#             The entity response object dictionary with related links included.
#         """
#
#         return dict(
#             entity,
#             **{
#                 f'{name}_link': self.get_ref(
#                     entity['id'] if is_collection is True else None,
#                     related_component
#                 ) for name, related_component in self.get_related_components().items()
#             }
#         )
#
#     def build_self_links(self, entity: dict, is_collection: bool = False) -> dict:
#         """
#         Creates SensorThings self-referential link.
#
#         Parameters
#         ----------
#         entity : dict
#             The entity response object dictionary.
#         is_collection : bool
#             Includes the entity ID in the reference URL if True, and omits it if False.
#
#         Returns
#         -------
#         dict
#             The entity response object dictionary with the self link included.
#         """
#
#         return dict(
#             entity,
#             **{
#                 'self_link': self.get_ref(entity['id'] if is_collection is True else None)
#             }
#         )
#
#     def build_next_link(self, top: int, skip: int) -> str:
#         """
#         Creates SensorThings next link for paginated responses.
#
#         Parameters
#         ----------
#         top : int
#             An integer representing how many records are returned in the response.
#         skip : int
#             An integer representing how many records are skipped in the response.
#
#         Returns
#         -------
#         str
#             A URL that links to the next dataset following the subset of data in the current response.
#         """
#
#         return f'{self.get_ref()}?$top={top}&$skip={top+skip}'
#
#     @abstractmethod
#     def resolve_entity_id_chain(self, entity_chain: List[Tuple[str, Union[UUID, int, str]]]) -> \
#             (bool, Optional[Union[UUID, int, str]]):
#         """
#         Abstract method for resolving an entity chain passed to the API.
#
#         SensorThings supports nested references to entities in URL paths. The Django HydroThings middleware will check
#         the nested components to ensure each one is related to its parent and build a list of IDs that need to be
#         verified by this method.
#
#         Parameters
#         ----------
#         entity_chain : list
#             A list of tuples representing the entity chain where the first object in the tuple is a string representing
#             the component name, and the second object in the tuple is a string, int, or UUID representing the entity ID.
#
#         Returns
#         -------
#         bool
#             Returns True if the entity chain could be fully resolved, and False if any part of the entity chain could
#             not be found or resolved.
#         """
#
#         pass
#
#     @abstractmethod
#     def list(
#             self,
#             filters,
#             count,
#             order_by,
#             skip,
#             top,
#             select,
#             expand
#     ) -> dict:
#         """
#         Abstract method for handling GET collection requests.
#
#         This method should return a dictionary representing a collection of entities for this component and apply all
#         the given query parameters.
#
#         Parameters
#         ----------
#         filters
#
#         count : bool
#             If True, the pre-pagination result count should be included in the response. If False, the count should be
#             omitted.
#         order_by
#
#         skip : int
#             An integer representing the number of records to skip in the response.
#         top : int
#             An integer representing the number of records the response should be limited to.
#         select
#             Represents a subset of this component's fields to include in the response.
#         expand
#             Represents related components whose fields should be included in the response.
#
#         Returns
#         -------
#         dict
#             A dictionary object representing the SensorThings GET collection response.
#         """
#
#         pass
#
#     @abstractmethod
#     def get(
#             self,
#             entity_id: str,
#             expand
#     ) -> Optional[dict]:
#         """
#         Abstract method for handling GET entity requests.
#
#         This method should return a dictionary representing an entity with the given entity ID.
#
#         Parameters
#         ----------
#         entity_id : str
#             The ID of the entity to be returned.
#         expand
#             Represents related components whose fields should be included in the response.
#
#         Returns
#         -------
#         dict
#             A dictionary object representing the SensorThings GET entity response.
#         """
#
#         pass
#
#     @abstractmethod
#     def create(
#             self,
#             entity_body: BasePostBody,
#     ) -> str:
#         """
#         Abstract method for handling POST entity requests.
#
#         This method should create a new entity and return the ID of the created entity.
#
#         Parameters
#         ----------
#         entity_body : BasePostBody
#             A dictionary object containing the attributes of the entity that will be created.
#
#         Returns
#         -------
#         str
#             The ID of the newly created entity.
#         """
#
#         pass
#
#     @abstractmethod
#     def update(
#             self,
#             entity_id: str,
#             entity_body: BasePatchBody
#     ) -> str:
#         """
#         Abstract method for handling PATCH entity requests.
#
#         This method should update an existing entity with the attributes included in the entity_body and return the ID
#         of the updated entity.
#
#         Parameters
#         ----------
#         entity_id : str
#             The ID of the entity to be updated.
#         entity_body : BasePatchBody
#             A dictionary object containing the attributes of the entity that will be updated.
#
#         Returns
#         -------
#         str
#             The ID of the updated entity.
#         """
#
#         pass
#
#     @abstractmethod
#     def delete(
#             self,
#             entity_id
#     ) -> None:
#         """
#         Abstract method for handling DELETE entity requests.
#
#         This method should delete an existing entity with the given entity_id.
#
#         Parameters
#         ----------
#         entity_id : str
#             The ID of the entity t obe deleted.
#
#         Returns
#         -------
#         None
#         """
#
#         pass


class SensorThingsRequest(HttpRequest):
    """
    The SensorThings request class.

    This class extends Django's HttpRequest class to include an engine class, component name, component path, and an
    entity_chain tuple. These attributes should be added to the request in the SensorThings middleware before calling a
    view function.
    """

    engine: SensorThingsBaseEngine
    auth: str
    component: str
    component_path: List[str]
    entity_chain: List[Tuple[str, Union[UUID, int, str]]]
