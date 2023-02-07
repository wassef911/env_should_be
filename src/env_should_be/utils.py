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




def is_valid_env(expected: dict, actual: dict) -> set:
    descriptions: list[Description] = [Length, MinLength, MaxLength, Regex, Option]
    invalid_vars = set()
    for key, value in expected.items():
        actual_value = actual[key]
        for cls in descriptions:
            if cls.get_name() in value:
                description = cls(value[cls.get_name()])
                if not description.does_pass(actual_value):
                    invalid_vars.add(tuple([key, description.get_name()]))
    return invalid_vars
