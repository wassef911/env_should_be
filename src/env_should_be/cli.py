#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import subprocess
from json.decoder import JSONDecodeError

from .exception import CallBackNotRunning
from .exception import EnvironmentFileNotLoading
from .utils import *

logging.basicConfig(
    level=logging.INFO,  # Adjust the log level as needed
    format="%(levelname)s: %(message)s",
)

arguments = [
    {
        "dest": "description",
        "option_strings": ["-d", "--description"],
        "nargs": "+",
        "help": "<Required> either one or multiple paths for description files.",
        "required": True,
    },
    {
        "dest": "fail_silently",
        "option_strings": ["-fs", "--fail-silently"],
        "type": bool,
        "help": "<Optional> will return an exit status of 0 even if the description(s) fail to match the current env (still triggers the callback).",
        "required": False,
        "default": False,
    },
    {
        "dest": "env_file",
        "option_strings": ["-e", "--env-file"],
        "type": str,
        "help": "<Optional> not specifying a path to a specific env file to validate description(s) against, environment variables in the current shell will be loaded instead.",
        "required": False,
        "default": None,
    },
    {
        "dest": "callback",
        "option_strings": ["-cb", "--callback"],
        "type": str,
        "help": "<Optional> a callback script to be executed an environment fails to match the a description. (still triggered on fail-silently)",
        "required": False,
        "default": None,
    },
]


class Namespace:
    description: list[str]
    fail_silently: bool
    env_file: bool
    callback: str


def main():
    parser = argparse.ArgumentParser(
        description="How should your environment be?")
    for arg in arguments:
        parser.add_argument(*arg["option_strings"], **arg)
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
    errors = get_errors_for(env, args.description)
    if errors.__len__() > 0:
        for e in errors:
            logging.warning(f"Env Not matching {e.description_path}")
            for variable, fails in e.errors:
                logging.error(f"\n {variable}, failing to match {fails}")
        if args.callback != None:
            try:
                subprocess.run([args.callback])
            except Exception as exc:
                raise CallBackNotRunning(
                    f"couldn't the callback script: {args.callback}, {exc}"
                )
        if not args.fail_silently:
            exit(1)
    exit(0)


if __name__ == "__main__":
    main()
