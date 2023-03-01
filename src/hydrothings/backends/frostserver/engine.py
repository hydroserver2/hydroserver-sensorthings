import requests
from hydrothings.engine import SensorThingsAbstractEngine
from hydrothings.settings import FROST_BASE_URL


class FrostServerEngine(SensorThingsAbstractEngine):

    def __init__(self, host: str, scheme: str, path: str, version: str, component: str, component_path: str):
        self.host = host
        self.scheme = scheme
        self.path = path
        self.version = version
        self.component = component
        self.component_path = component_path
        self.frost_url = '/'.join((FROST_BASE_URL, f'v{self.version}', self.component_path,))

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
