from __future__ import annotations

import os
from json import load
from typing import List

from .description import *


def load_env_file(file_path) -> dict:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'{file_path} does not exist.')
    with open(file_path) as file:
        env_vars = {}
        for line in file:
            if not line.startswith('#'):
                key, value = line.strip().split('=')
                env_vars[key] = value
    return env_vars


def load_all_env_vars() -> dict:
    env_vars = {}
    for key, value in os.environ.items():
        env_vars[key] = value
    return env_vars


def load_json_file(file_path: str) -> dict:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'{file_path} does not exist.')
    with open(file_path) as file:
        json_data = load(file)
    return json_data


def is_valid_env(expected_env: dict, actual_env: dict) -> Optional[True]:
    invalid_vars = []
    klass: Description = None  # just to type hint
    for key, values in expected_env.items():
        fails: list[str] = []
        for klass in [Length, MinLength, MaxLength, Regex, Option]:
            if klass.get_name() not in values:
                # user did not use this description
                continue
            description = klass(values[klass.get_name()])
            if not description.does_pass(actual_env.get(key, None)):
                fails.append(klass.get_name())
        if fails.__len__() > 0:
            invalid_vars.append([key, fails])
    invalid_vars.sort(key=lambda fail: fail[0])
    return invalid_vars if invalid_vars.__len__() > 0 else True
