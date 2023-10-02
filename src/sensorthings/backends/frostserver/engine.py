import requests
from uuid import UUID
from typing import List, Union, Tuple
from sensorthings.engine import SensorThingsAbstractEngine
from sensorthings.settings import FROST_BASE_URL


class FrostServerEngine(SensorThingsAbstractEngine):

    def __init__(self, host: str, scheme: str, path: str, version: str, component: str, component_path: str):
        self.host = host
        self.scheme = scheme
        self.path = path
        self.version = version
        self.component = component
        self.component_path = component_path
        self.frost_url = '/'.join((FROST_BASE_URL, f'v{self.version}', self.component_path,))

    def resolve_entity_id_chain(self, entity_chain: List[Tuple[str, Union[UUID, int, str]]]) -> bool:
        return True

    def list(
            self,
            filters,
            count,
            order_by,
            skip,
            top,
            select,
            expand
    ) -> requests.Response:

        response = requests.get(self.frost_url)

        return response

    def get(
            self,
            entity_id,
            component=None
    ) -> requests.Response:

        response = requests.get(self.frost_url)

        return response

    def create(
            self,
            entity_body,
            component=None
    ) -> str:
        # response = requests.post(self.frost_url, data=entity_body)
        # print(response)

        return '0'

    def update(
            self,
            entity_id,
            entity_body
    ) -> str:
        return '0'

    def delete(
            self,
            entity_id
    ) -> None:
        return None
