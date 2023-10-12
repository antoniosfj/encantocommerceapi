from django.db import models
from collections.abc import Iterable


class PathValue:
    def __init__(self, value, splitter='.') -> None:
        if isinstance(value, str):
            self.value = value.split(splitter)
        elif isinstance(value, Iterable):
            self.value = [x for x in value]
        else:
            raise ValueError('Invalid value for PathValue')

    def __str__(self) -> str:
        return '.'.join(self.value)


class PathField(models.Field):
    def db_type(self, connection):
        if connection.vendor == "postgresql":
            return "ltree"
        raise type('InvalidDbType', (Exception,), {})('It MUST BE a postgresql connection!')

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return PathValue(value)

    def to_python(self, value):
        if isinstance(value, PathValue) or value is None:
            return value

        return PathField(value)

    def get_prep_value(self, value):
        if not value:
            return value
        return str(PathValue(value))
