import datetime
from typing import Any, Optional, Type, Union

import ujson
from tortoise.exceptions import BaseORMException, ConfigurationError
from tortoise.fields import CharField, DatetimeField, Field
from tortoise.models import Model
from tortoise.validators import MaxLengthValidator


class ArrayField(Field, list, tuple, set):
    def to_db_value(
        self, value: Optional[Union[list, tuple, set]], instance
    ) -> Optional[str]:
        if instance and not instance._saved_in_db:
            return value
        if value is None:
            return None
        if isinstance(value, (list, tuple, set)):  # pylint: disable=W1116
            return value
        else:
            raise BaseORMException("Non Iterable value provided for ArrayField ")

    def to_python_value(self, value: Optional[Union[str, list]]) -> Optional[list]:
        if value is None or isinstance(value, list):
            return value
        else:
            return ujson.loads(value)


class TextArrayField(ArrayField):
    pass


class IntArrayField(ArrayField):
    pass


class CustomTextField(CharField):
    def __init__(self, max_length: int = 100, **kwargs: Any) -> None:
        if int(max_length) < 1:
            raise ConfigurationError("'max_length' must be >= 1")
        self.max_length = int(max_length)
        super().__init__(max_length, **kwargs)
        self.validators.append(MaxLengthValidator(self.max_length))

    @property
    def SQL_TYPE(self) -> str:  # type: ignore
        return f"text({self.max_length})"


class CITextField(CustomTextField):
    pass


class NaiveDatetimeField(DatetimeField):
    skip_to_python_if_native = True

    class _db_postgres:  # noqa
        SQL_TYPE = "TIMESTAMP"

    def to_python_value(self, value: Any) -> Optional[datetime.datetime]:
        value = super().to_python_value(value)

        if value is None:
            return value

        return self.to_naive(value)

    # pylint: disable=R0201
    def to_naive(self, value: datetime.datetime) -> datetime.datetime:
        if value.tzinfo is None:
            return value

        value = value.astimezone(datetime.timezone.utc)

        return value.replace(tzinfo=None)

    def to_db_value(
        self,
        value: Optional[datetime.datetime],
        instance: Union[Type[Model], Model],
    ) -> Optional[datetime.datetime]:
        value = super().to_db_value(value, instance)

        if value is None:
            return value

        return self.to_naive(value)
