from __future__ import annotations

import os
from json import load

def load_env_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'{file_path} does not exist.')
    with open(file_path) as file:
        env_vars = {}
        for line in file:
            if not line.startswith('#'):
                key, value = line.strip().split('=')
                env_vars[key] = value
    return env_vars


def load_all_env_vars():
    env_vars = {}
    for key, value in os.environ.items():
        env_vars[key] = value
    return env_vars

def load_json_description(file_path)-> dict:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    with open(file_path, 'r') as file:
        json_data = load(file)
    return json_data

def is_valid_env(expected:dict, actual: dict) -> set:
    invalid_vars = set()
    for key, value in expected.items():
        if key not in actual:
            if value.get('required', False):
                invalid_vars.add(tuple([key,'required']))
            continue

        actual_value = actual[key]
        if 'length' in value:
            if len(actual_value) != value['length']:
                invalid_vars.add(tuple([key,'length']))
            continue

        if 'min_length' in value:
            if len(actual_value) < value['min_length']:
                invalid_vars.add(tuple([key,'min_length']))
            continue

        if 'max_length' in value:
            if len(actual_value) > value['max_length']:
                invalid_vars.add(tuple([key,'max_length']))
            continue

        if 'regex' in value:
            import re
            if not re.match(value['regex'], actual_value):
                invalid_vars.add(tuple([key,'regex']))
            continue

        if 'options' in value:
            if actual_value not in value['options']:
                invalid_vars.add(tuple([key,'options']))
            continue
        # TODO: constant/IsInt/IsString/if_other_variable/if_not_other_variable
    return invalid_vars
