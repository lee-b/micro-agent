#!/usr/bin/env python3

import argparse
import logging
import pathlib
import sys

from agent import agi


logger = logging.getLogger(__name__)


def build_arg_parser():
    cwd = pathlib.Path(".").absolute()
    default_app_dir = cwd / "app"

    parser = argparse.ArgumentParser()

    parser.add_argument("--directory", "-d", default=default_app_dir, help="The directory containing the project code", type=pathlib.Path)
    parser.add_argument("--purpose", "-p", help="The purpose that the agent should pursue, against the project directory.")
    parser.add_argument("--purpose-file", "-P", help="A text file containing the purpose that the agent should pursue, against the project directory.")
    parser.add_argument("--openai-server-url", "-u", default="http://localhost:8000/v1", help="The address of the OpenAI-compatible server to call")

    return parser


def load_purpose(fpath: pathlib.Path) -> str:
    with open(fpath, 'r') as fp:
        purpose = fp.read()

    return purpose


def main():
    logging.basicConfig()

    arg_parser = build_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])

    if not args.directory.is_dir():
        logger.error("%s is not a valid directory!", args.directory)
        return 1

    if args.purpose:
        purpose = args.purpose
    elif args.purpose_file:
        purpose = load_purpose(args.purpose_file)
    else:
        logger.error("No purpose given!  Try --help")
        return 1

    agi.run(
        purpose,
        args.directory,
        args.openai_server_url,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())

