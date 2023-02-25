from hydrothings.engine import SensorThingsAbstractEngine


class SensorThingsEngineODM2(SensorThingsAbstractEngine):

    def __init__(self, host: str, scheme: str, path: str, component: str):
        self.host = host
        self.scheme = scheme
        self.path = path
        self.component = component

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
        return {}

    def get(
            self,
            entity_id,
            component=None
    ) -> dict:
        return {}

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
