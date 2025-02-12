#!/usr/bin/python3
"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-27

Author: Penaz
"""
import argparse
import importlib
import logging
from pathlib import Path

from libs.commands import find_commands, registry

LOGGER = logging.getLogger(__name__)


def register_commands():
    """
    Register all available commands
    """
    commands = find_commands(Path(__file__).parent.resolve())
    for command_name in commands:
        importlib.import_module(f"commands.{command_name}")


def execute_command(command_name, cmd_args):
    """
    Executes the command in the command line
    """
    LOGGER.debug("Executing command %s", command_name)
    cmd_instance = registry.commands[command_name]()
    cmd_instance(cmd_args)


if __name__ == "__main__":
    register_commands()
    parser = argparse.ArgumentParser(prog="VirtIAC")
    parser.add_argument(
        "-v", "--verbose", help="Enables debugging logging output",
        action="store_true", dest="verbose"
    )
    subparsers = parser.add_subparsers(title="Subcommands", required=True)
    for cmdname, cmd in registry.commands.items():
        cmd.register_parser_subcommands(subparsers)
    arguments = parser.parse_args()
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(levelname)-10s | %(message)s"
    if arguments.verbose:
        LOG_LEVEL = logging.DEBUG
        LOG_FORMAT = (
            "%(asctime)s | %(levelname)-10s |"
            " %(module)s:%(funcName)s - %(message)s"
        )
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT
    )
    if not arguments.command:
        parser.print_help()
    execute_command(arguments.command, arguments)
