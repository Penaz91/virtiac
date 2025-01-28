"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-27

Author: Penaz
"""
import pkgutil


def find_commands(path):
    """
    Automatically finds commands in the command folder
    """
    commands_dir = path / "commands"
    return {
        name
        for _, name, is_package in pkgutil.iter_modules([commands_dir])
        if not is_package and not name.startswith("_")
    }


class CommandRegistry:
    """
    Class used as command registry
    """
    commands = {}

    def register(self, name):
        """
        Registers a new command
        """
        def wrapped_registration(klass):
            self.commands[name] = klass
        return wrapped_registration


registry = CommandRegistry()
