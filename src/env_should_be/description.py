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
    "IsNumber",
    "IsGreaterThanEq",
    "IsLowerThanEq",
    "IsHttp",
    "IsHttps",
    "IsIpv4",
    "IsIpv6",
    "IsEmail",
    "IsUuid",
)

import re
from abc import ABC
from abc import abstractmethod
from typing import Any, List
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
        return not None and isinstance(value, bool)


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
            return True and isinstance(value, str)
        except Exception:
            return False

    def does_pass(self, actual: str | None) -> bool:
        return (
            actual != None
            and isinstance(actual, str)
            and (re.match(self.value, actual) != None)
        )


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
        return not isinstance(actual, bool) and isinstance(actual, int) == self.value


class IsStr(Boolean):
    def does_pass(self, actual):
        return isinstance(actual, str) == self.value


class IsFloat(Boolean):
    def does_pass(self, actual):
        return isinstance(actual, float) == self.value


class IsNumber(Boolean):
    def does_pass(self, actual):
        case1 = IsFloat(self.value)
        case2 = IsInt(self.value)
        return case1.does_pass(actual) or case2.does_pass(actual)


class IsGreaterThanEq(Description):
    def is_valid(self, value):
        return (
            not None
            and not isinstance(value, bool)
            and (isinstance(value, int) or isinstance(value, float))
        )

    def does_pass(self, actual):
        case1 = IsNumber(True)
        return case1.does_pass(actual) and (actual >= self.value)


class IsLowerThanEq(IsGreaterThanEq):
    def does_pass(self, actual):
        case1 = IsNumber(True)
        return case1.does_pass(actual) and (actual <= self.value)


class IsHttp(Boolean):
    def does_pass(self, actual):
        i = Regex(
            "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        )
        return i.does_pass(actual)


class IsHttps(Boolean):
    def does_pass(self, actual):
        i = Regex(
            "^https:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        )
        return i.does_pass(actual)


class IsIpv4(Boolean):
    def does_pass(self, actual):
        i = Regex(
            "^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        )
        return i.does_pass(actual)


class IsIpv6(Boolean):
    def does_pass(self, actual):
        i = Regex(
            "^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$"
        )
        return i.does_pass(actual)


class IsEmail(Boolean):
    def does_pass(self, actual):
        i = Regex("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        return i.does_pass(actual)


class IsUuid(Boolean):
    def does_pass(self, actual):
        i = Regex(
            "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
        )
        return i.does_pass(actual)
