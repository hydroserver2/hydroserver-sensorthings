from uuid import UUID
from pydantic import Field, Extra, HttpUrl, validator
from typing import Union
from ninja import Schema
from hydrothings.validators import nested_entities_check, whitespace_to_none


class EntityId(Schema):
    id: UUID = Field(..., alias='@iot.id')


class NestedEntity(Schema):

    class Config:
        extra = Extra.allow


class EntityNotFound(Schema):
    message: str


class BasePostBody(Schema):

    _nested_entity_validator = validator(
        '*',
        allow_reuse=True,
        check_fields=False
    )(nested_entities_check)

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
    next_link: Union[HttpUrl, None] = Field(None, alias='@iot.nextLink')

    class Config:
        allow_population_by_field_name = True


class BaseGetResponse(Schema):
    id: UUID = Field(..., alias='@iot.id')
    self_link: HttpUrl = Field(..., alias='@iot.selfLink')

    class Config:
        allow_population_by_field_name = True


class Filters(Schema):
    filters: str = Field(None, alias='$filter')
    count: bool = Field(None, alias='$count')
    order_by: str = Field(None, alias='$orderby')
    skip: int = Field(0, alias='$skip')
    top: int = Field(None, alias='$top')
    select: str = Field(None, alias='$select')
    expand: str = Field(None, alias='$expand')
    result_format: str = Field(None, alias='$resultFormat')
