from ninja import Router
from pydantic import AnyHttpUrl
from typing import Union, List
from sensorthings.schemas import PermissionDenied, EntityNotFound


class SensorThingsRouter(Router):
    def st_list(self, route, response_schema, url_name=None):
        return super(SensorThingsRouter, self).get(
            route,
            response={
                200: response_schema
            },
            by_alias=True,
            exclude_unset=True,
            url_name=url_name
        )

    def st_get(self, route, response_schema, url_name=None):
        return super(SensorThingsRouter, self).get(
            route,
            response={
                200: response_schema,
                403: PermissionDenied,
                404: EntityNotFound
            },
            by_alias=True,
            exclude_unset=True,
            url_name=url_name
        )

    def st_post(self, route, url_name=None):
        return super(SensorThingsRouter, self).post(
            route,
            response={
                201: Union[None, List[AnyHttpUrl]],
                403: PermissionDenied
            },
            url_name=url_name
        )

    def st_patch(self, route, url_name=None):
        return super(SensorThingsRouter, self).patch(
            route,
            response={
                204: None,
                403: PermissionDenied,
                404: EntityNotFound
            },
            url_name=url_name
        )

    def st_delete(self, route, url_name=None):
        return super(SensorThingsRouter, self).delete(
            route,
            response={
                204: None,
                403: PermissionDenied,
                404: EntityNotFound
            },
            url_name=url_name
        )
