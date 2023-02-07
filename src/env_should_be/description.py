import re
from abc import ABC, abstractmethod
from typing import Any

from abc import ABC, abstractmethod
from typing import Any

class Description(ABC):

    def __init__(self, value: Any):
        self.value = value

    @staticmethod
    def to_snake_case(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('__([A-Z])', r'_\1', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()

    @staticmethod
    def get_name() -> str:
        return Description.to_snake_case(Description.__name__)

    @abstractmethod
    def is_valid(self, value: Any) -> bool:
        pass

    @property
    def value(self) -> Any:
        return self.__value

    @value.setter
    def value(self, val: Any):
        if self.is_valid(val):
            self.__value = val
        else:
            raise ValueError("Invalid value")

    @abstractmethod
    def does_pass(self) -> bool:
        pass

class Length(Description):

    @staticmethod
    def get_name() -> str:
        return Description.to_snake_case(Length.__name__)

    def is_valid(self, value):
        return isinstance(value, int) and value > 0

    def does_pass(self, actual: str):
        return actual.__len__() == self.value


class MinLength(Length):

    @staticmethod
    def get_name() -> str:
        return Description.to_snake_case(MinLength.__name__)

    def does_pass(self, actual: str):
        return actual.__len__() > self.value


class MaxLength(Length):
    @staticmethod
    def get_name() -> str:
        return Description.to_snake_case(MaxLength.__name__)

    def does_pass(self, actual: str):
        return actual.__len__() < self.value


class Regex(Description):
    @staticmethod
    def get_name() -> str:
        return Description.to_snake_case(Regex.__name__)

    def is_valid(self, value):
        try:
            re.compile(value)
            return True
        except re.error:
            return False

    def does_pass(self, actual: str):
        return re.match(self.value, actual)


class Option(Description):
    @staticmethod
    def get_name() -> str:
        return Description.to_snake_case(Option.__name__)

    def is_valid(self, value: list):
        return hasattr(value, "__iter__") and value.__len__() > 0

    def does_pass(self, actual: str):
        return actual in self.value


# TODO: constant/IsInt/IsString/if_other_variable/if_not_other_variable
