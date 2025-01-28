"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-28

Author: Penaz
"""
import json
import logging
from os import getcwd
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def find_machine_file():
    """
    Finds a virtiac.json file from the current working directory up
    """
    LOGGER.info("Looking for virtiac.json file")
    current_path = Path(getcwd())
    while current_path != Path.home():
        LOGGER.debug("Looking for virtiac.json in %s", current_path)
        file_path = current_path / "virtiac.json"
        if file_path.is_file():
            LOGGER.debug("Virtiac file found in %s", file_path)
            return file_path.resolve()
        current_path = current_path.parent
    LOGGER.info("Virtiac file not found")
    raise RuntimeError("Virtiac file not found and no domain specified")


def get_machine_file():
    """
    Finds a virtiac.json file and parses its json
    """
    machine_file = find_machine_file()
    with open(machine_file, "r", encoding="utf-8") as fh:
        return json.load(fh)
