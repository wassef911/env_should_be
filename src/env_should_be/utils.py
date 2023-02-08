from __future__ import annotations

import os
from json import load
from .description import *


def load_env_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    with open(file_path) as file:
        env_vars = {}
        for line in file:
            if not line.startswith("#"):
                key, value = line.strip().split("=")
                env_vars[key] = value
    return env_vars


def load_all_env_vars():
    env_vars = {}
    for key, value in os.environ.items():
        env_vars[key] = value
    return env_vars


def load_json_description(file_path) -> dict:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    with open(file_path, "r") as file:
        json_data = load(file)
    return json_data




def is_valid_env(expected_env: dict, actual: dict) -> set:
    validations: list[Description] = [Length, MinLength, MaxLength, Regex, Option]
    invalid_vars = set()
    for key, value in expected_env.items():
        for cls in validations:
            validation_name = cls.get_name()
            if validation_name in value:
                instance = cls(value[validation_name])
                if not instance.does_pass(actual[key]):
                    invalid_vars.add(tuple([key, validation_name]))
    return invalid_vars
