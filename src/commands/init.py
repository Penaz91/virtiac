"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-02-06

Author: Penaz
"""
import logging
from os import getcwd
from pathlib import Path
from shutil import copy

from libs.commands import registry

LOGGER = logging.getLogger(__name__)


@registry.register("init")
class InitCommand:
    """
    Initializes domains by writing a virtiac.json file
    """
    LOGGER.info("Initializing new virtiac.json file")
    path = Path(__file__).parent.parent.resolve() / "default.json"
    destination = Path(getcwd()) / "virtiac.json"
    if destination.is_file():
        LOGGER.error("Virtiac.json file already exists")
    copy(path, destination)
    LOGGER.info("Default Virtiac.json has copied to the project folder")

    def __call__(self, arguments):
        """
        Creates a virtiac.json file where called
        """

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "init", help="Create a new virtiac.json file"
        )
        parser.set_defaults(command="init")
