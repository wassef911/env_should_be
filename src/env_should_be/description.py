from __future__ import annotations

__all__ = (
    "Boolean",
    "Length",
    "MinLength",
    "MaxLength",
    "Regex",
    "Option",
    "Constant",
    "IsInt",
    "IsStr",
    "IsFloat",
)

import re
from abc import ABC
from abc import abstractmethod
from typing import Optional, Any, List
from .exception import ValueUnassignableToDescription


class Description(ABC):
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def is_valid(self, value) -> bool:
        pass

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if self.is_valid(val):
            self.__value = val
            return
        raise ValueUnassignableToDescription(
            f"Value {val} is Invalid, can't be assigned to {self.__class__.__name__} "
        )

    @abstractmethod
    def does_pass(self, actual: str | None) -> bool:
        pass


class Boolean(Description):
    def is_valid(self, value):
        return isinstance(value, bool)


class Length(Description):
    def is_valid(self, value):
        return isinstance(value, int) and value > 0

    def does_pass(self, actual: str | None) -> bool:
        return (
            actual is not None
            and hasattr(actual, "__len__")
            and actual.__len__() == self.value
        )


class MinLength(Length):
    def does_pass(self, actual: str | None) -> bool:
        return (
            isinstance(actual, str)
            and hasattr(actual, "__len__")
            and actual.__len__() >= self.value
        )


class MaxLength(Length):
    def does_pass(self, actual: str | None) -> bool:
        return (
            isinstance(actual, str)
            and hasattr(actual, "__len__")
            and actual.__len__() <= self.value
        )


class Regex(Description):
    def is_valid(self, value):
        try:
            re.compile(value)
            return True
        except Exception:
            return False

    def does_pass(self, actual: str | None) -> bool:
        return actual != None and re.match(self.value, actual)


class Option(Description):
    def is_valid(self, value: list[Any]):
        return (
            isinstance(value, List)
            and hasattr(value, "__iter__")
            and value.__len__() > 0
        )

    def does_pass(self, actual: str | None) -> bool:
        return actual in self.value


class Constant(Description):
    def is_valid(self, value):
        try:
            x = str(value)
            return x.__len__() > 0  # can't use an empty string!
        except Exception:
            return False

    def does_pass(self, actual: str | None) -> bool:
        return str(actual) == str(self.value)


class IsInt(Boolean):
    def does_pass(self, actual):
        return isinstance(actual, int) == self.value


class IsStr(Boolean):
    def does_pass(self, actual):
        return isinstance(actual, str) == self.value


class IsFloat(Boolean):
    def does_pass(self, actual):
        return isinstance(actual, float) == self.value
