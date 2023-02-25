import inspect
import hydrothings.components as core_components
import hydrothings.schemas as core_schemas
from pydantic import BaseModel


def nested_entities_check(value, field):
    """
    Validation for nested components.

    Runs validation on nested components in request bodies to avoid circular relationships in the API documentation.

    :param value: The input value.
    :param field: The field being validated.
    :return value: The output value.
    """

    nested_class_name = field.field_info.extra.get('nested_class')

    if nested_class_name:
        nested_class = getattr(core_components, nested_class_name)

        if isinstance(value, list):
            value = [
                nested_class(**sub_value.dict()) if isinstance(sub_value, core_schemas.NestedEntity) else sub_value
                for sub_value in value
            ]

        elif isinstance(value, core_schemas.NestedEntity):
            value = nested_class(**value.dict())

    return value


def whitespace_to_none(value):
    """
    Validation for whitespace values.

    Checks if string values are blank or only whitespace and converts them to NoneType.

    :param value: The input value.
    :return value: The output value.
    """

    if isinstance(value, str) and (value == '' or value.isspace()):
        return None

    return value


def allow_partial(*fields):
    """
    Declares fields of a Pydantic model as optional.

    This decorator can be used to update required fields of a Pydantic model to be optional. This can be used in
    conjunction with exclude_unset to allow for missing fields, but still adhere to not_null requirements, such as when
    partially updating a datastore.

    :param fields: All fields which should be made optional. If none are passed, all fields will be made optional.
    :return dec: The optional class decorator.
    """

    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)

    return dec
