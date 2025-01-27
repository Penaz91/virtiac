"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-27

Author: Penaz
"""
from os import getcwd

from libs.commands import registry


@registry.register("cwd")
class SecondCommand:

    def __call__(self, arguments):
        """
        Shows current working directory
        """
        print(getcwd())

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Adds the argument subparser
        """
        parser = subparsers.add_parser("cwd")
        parser.set_defaults(command="cwd")
