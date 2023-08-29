from __future__ import annotations

import argparse

__version__ = '0.1.0'

from .utils import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='How should your environment be ?')
    parser.add_argument(
        '-l', '--like', nargs='+', help='<Required> Set flag', required=True
    )
    parser.add_argument(
        '-fs',
        '--fail-silently',
        type=bool,
        help='<Required> Set flag',
        required=False,
        default=False,
    )
    parser.add_argument(
        '-e',
        '--env-file',
        type=str,
        help='<Required> Set flag',
        required=False,
        default=False,
    )
    try:
        args = parser.parse_args()
        print(args)
        env = load_env_file(
            args.env_file) if args.env_file else load_all_env_vars()
        description = load_json_description(args.env_file)
        errors = is_valid_env(description, env)
        if errors.__len__():
            print(list(errors))
        print(description)
        if args.fail_silently:
            exit(0)
        else:
            exit(1)
    except FileNotFoundError as e:
        pass
    except Exception as e:
        pass
