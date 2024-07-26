from ninja import Router
from typing import Union, List, Type
from sensorthings.schemas import PermissionDenied, EntityNotFound
from sensorthings.types import AnyHttpUrlString


class SensorThingsRouter(Router):
    """
    A custom router for the SensorThings API that extends Django Ninja's Router.
    It provides methods for common HTTP operations with standardized response schemas.
    """

    def st_list(self, route, response_schema: Type, *args, **kwargs):
        """
        Define a GET endpoint for listing resources.

        Parameters
        ----------
        route : str
            The route path for the endpoint.
        response_schema : Schema
            The tuple of response schemas for a successful response.

        Returns
        -------
        callable
            The endpoint decorated as a GET operation.
        """

        return super(SensorThingsRouter, self).get(
            route,
            *args,
            response={
                200: Union[(response_schema,)]
            },
            by_alias=True,
            exclude_unset=True,
            **kwargs
        )

    def st_get(self, route, response_schema, *args, **kwargs):
        """
        Define a GET endpoint for retrieving a single resource.

        Parameters
        ----------
        route : str
            The route path for the endpoint.
        response_schema : Schema
            The tuple of response schemas for a successful response.

        Returns
        -------
        callable
            The endpoint decorated as a GET operation.
        """

        return super(SensorThingsRouter, self).get(
            route,
            *args,
            response={
                200: Union[(response_schema, str,)],
                403: PermissionDenied,
                404: EntityNotFound
            },
            by_alias=True,
            exclude_unset=True,
            **kwargs
        )

    def st_post(self, route, *args, **kwargs):
        """
        Define a POST endpoint for creating a new resource.

        Parameters
        ----------
        route : str
            The route path for the endpoint.

        Returns
        -------
        callable
            The endpoint decorated as a POST operation.
        """

        kwargs = {k: v for k, v in kwargs.items() if k not in ['response', 'response_schema']}
        return super(SensorThingsRouter, self).post(
            route,
            *args,
            response={
                201: Union[None, List[AnyHttpUrlString]],
                403: PermissionDenied
            },
            **kwargs
        )

    def st_patch(self, route, *args, **kwargs):
        """
        Define a PATCH endpoint for partially updating a resource.

        Parameters
        ----------
        route : str
            The route path for the endpoint.

        Returns
        -------
        callable
            The endpoint decorated as a PATCH operation.
        """

        kwargs = {k: v for k, v in kwargs.items() if k not in ['response', 'response_schema']}
        return super(SensorThingsRouter, self).patch(
            route,
            *args,
            response={
                204: None,
                403: PermissionDenied,
                404: EntityNotFound
            },
            **kwargs
        )

    def st_delete(self, route, *args, **kwargs):
        """
        Define a DELETE endpoint for removing a resource.

        Parameters
        ----------
        route : str
            The route path for the endpoint.

        Returns
        -------
        callable
            The endpoint decorated as a DELETE operation.
        """

        kwargs = {k: v for k, v in kwargs.items() if k not in ['response', 'response_schema']}
        return super(SensorThingsRouter, self).delete(
            route,
            *args,
            response={
                204: None,
                403: PermissionDenied,
                404: EntityNotFound
            },
            **kwargs
        )
