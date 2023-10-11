import urllib.parse
from uuid import UUID
from pydantic import Field, Extra, AnyHttpUrl, validator
from typing import Union
from ninja import Schema
from sensorthings.validators import nested_entities_check, whitespace_to_none


class EntityId(Schema):
    id: UUID = Field(..., alias='@iot.id')

    class Config:
        allow_population_by_field_name = True


class NestedEntity(Schema):

    class Config:
        extra = Extra.allow


class EntityNotFound(Schema):
    message: str


class PermissionDenied(Schema):
    detail: str


class BasePostBody(Schema):

    _nested_entity_validator = validator(
        '*',
        allow_reuse=True,
        check_fields=False
    )(nested_entities_check)

    _whitespace_validator = validator(
        '*',
        allow_reuse=True,
        check_fields=False,
        pre=True
    )(whitespace_to_none)

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True


class BasePatchBody(Schema):

    _whitespace_validator = validator(
        '*',
        allow_reuse=True,
        check_fields=False,
        pre=True
    )(whitespace_to_none)

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True


class BaseListResponse(Schema):
    count: Union[int, None] = Field(None, alias='@iot.count')
    value: list = []
    next_link: Union[AnyHttpUrl, None] = Field(None, alias='@iot.nextLink')

    class Config:
        allow_population_by_field_name = True


class BaseGetResponse(Schema):
    id: UUID = Field(..., alias='@iot.id')
    self_link: AnyHttpUrl = Field(..., alias='@iot.selfLink')

    class Config:
        allow_population_by_field_name = True


class GetQueryParams(Schema):
    expand: str = Field(None, alias='$expand')


class ListQueryParams(GetQueryParams):
    filters: str = Field(None, alias='$filter')
    count: bool = Field(None, alias='$count')
    order_by: str = Field(None, alias='$orderby')
    skip: int = Field(0, alias='$skip')
    top: int = Field(None, alias='$top')
    select: str = Field(None, alias='$select')

    class Config:
        allow_population_by_field_name = True

    def get_query_string(self):
        """"""

        query_string = '&'.join([
            f'{model.alias}={urllib.parse.quote(str(getattr(self, field)), safe="~")}'
            for field, model in self.__fields__.items() if getattr(self, field, None) is not None
        ])

        if query_string:
            query_string = '?' + query_string

        return query_string
