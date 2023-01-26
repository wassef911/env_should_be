from __future__ import annotations
import os
import argparse

__version__ = '0.1.0'

from utils import load_env_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='How should your environment be ?')
    parser.add_argument('-l', '--like', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('-fs', '--fail-silently', type=bool, help='<Required> Set flag', required=False, default=False)
    args = parser.parse_args()
    print(args)
