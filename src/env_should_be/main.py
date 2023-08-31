#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from json.decoder import JSONDecodeError

from .exception import DescriptionFileNotLoading
from .exception import EnvironmentFileNotLoading
from .utils import *


class Namespace:
    description: list[str]
    fail_silently: bool
    env_file: bool


@dataclass
class EnvironmentError:
    description_path: str = None
    errors: list = None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='How should your environment be?')
    parser.add_argument(
        '-d',
        '--description',
        nargs='+',
        help='<Required> either one or multiple paths for description files.',
        required=True,
    )
    parser.add_argument(
        '-fs',
        '--fail-silently',
        type=bool,
        help='<Optional> will return an exit status of 0 even if the description(s) fail to match the current env (still triggers the fail_callback).',
        required=False,
        default=False,
    )
    parser.add_argument(
        '-e',
        '--env-file',
        type=str,
        help='<Optional> not specifying a path to a specific env file to valid description(s) against, environment variables in the current shell will be loaded instead.',
        required=False,
        default=None,
    )
    args: Namespace = parser.parse_args()
    if args.env_file:
        try:
            env = load_env_file(args.env_file)
        except (
            FileNotFoundError,
            ValueError,
            JSONDecodeError,
        ) as exc:
            raise EnvironmentFileNotLoading(
                f"couldn't load file at:{args.env_file}, {exc}"
            )
    else:
        env = load_all_env_vars()
    errors: list[EnvironmentError] = []
    for path in args.description:
        try:
            description: dict = load_json_file(path)
        except (
            FileNotFoundError,
            ValueError,
            JSONDecodeError,
        ) as exc:
            raise DescriptionFileNotLoading(
                f"couldn't load file at:{path}, {exc}")
        is_valid = is_valid_env(description, env)
        if is_valid != True:
            errors.append(EnvironmentError(
                description_path=path, errors=is_valid))

    if errors.__len__() and not args.fail_silently:
        for e in errors:
            print(f'Env Not matching {e.description_path}')
            for variable, fails in e.errors:
                print(f'\n {variable}, failing to match {fails}')
        exit(1)
    exit(0)
