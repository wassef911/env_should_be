from __future__ import annotations

import inspect
import os
import re
from dataclasses import dataclass
from dataclasses import field
from functools import wraps
from io import TextIOWrapper
from json import JSONDecodeError
from json import load

from yaml import safe_load
from yaml.scanner import ScannerError

from . import description as all_descriptions
from .exception import DescriptionFileNotLoading
from .exception import FileHasNoExtension
from .exception import RequiredVariableNotSet


@dataclass
class VariableError:
    description_path: str | None = None
    errors: list[VariableError] = field(default_factory=list)


def file_to_dictionary(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        file_path = args[0]
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")
        with open(file_path) as file:
            data: dict = func(*args, file=file, **kwargs)
        return data

    return wrapper


@file_to_dictionary
def load_env_file(file_path: str, file: TextIOWrapper = None) -> dict:
    if file == None:
        raise SystemError()
    env_vars = {}
    for line in file:
        if not line.startswith("#"):
            key, value = line.strip().split("=")
            env_vars[key] = value
    return env_vars


@file_to_dictionary
def load_yaml_file(file_path: str, file: TextIOWrapper = None) -> dict:
    if file == None:
        raise SystemError()
    return safe_load(file)


@file_to_dictionary
def load_json_file(file_path: str, file: TextIOWrapper = None) -> dict:
    if file == None:
        raise SystemError()
    return load(file)


def load_all_env_vars() -> dict:
    env_vars = {}
    for key, value in os.environ.items():
        env_vars[key] = value
    return env_vars


def get_file_extension(file_path) -> str:
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()


def to_snake_case(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def is_valid_env(expected_env: dict, actual_env: dict) -> True | None:
    invalid_vars = []
    for key, values in expected_env.items():
        fails: list[str] = []
        for name, klass in inspect.getmembers(all_descriptions):
            klass_name = to_snake_case(name)
            if klass_name not in values:
                # user did not use this description
                continue
            description = klass(values[klass_name])
            value = actual_env.get(key, None)
            is_required = values.get("required", True)
            if is_required and value == None:
                raise RequiredVariableNotSet(f"{key} is_required not but set")
            if value != None and not description.does_pass(value):
                fails.append(klass_name)
        if fails.__len__() > 0:
            invalid_vars.append([key, fails])
    invalid_vars.sort(key=lambda fail: fail[0])
    return invalid_vars if invalid_vars.__len__() > 0 else True


def get_errors_for(env: dict, descriptions: list[str]) -> list[VariableError]:
    errors: list[VariableError] = []
    for path in descriptions:
        extension = get_file_extension(path)
        try:
            if extension == ".json":
                description: dict = load_json_file(path)
            elif extension in [".yml", ".yaml"]:
                description: dict = load_yaml_file(path)
            else:
                raise FileHasNoExtension(
                    f"make sure the description file ends with: .json/.yaml/.yml"
                )
        except (
            FileNotFoundError,
            JSONDecodeError,
            ScannerError,
            ValueError,
        ) as exc:
            raise DescriptionFileNotLoading(
                f"couldn't load file at:{path}, {exc}")
        is_valid = is_valid_env(description, env)
        if is_valid != True:
            errors.append(VariableError(
                description_path=path, errors=is_valid))
    return errors
