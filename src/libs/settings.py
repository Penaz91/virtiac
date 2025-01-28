"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-27

Author: Penaz
"""
import json
import logging
from os.path import isfile
from pathlib import Path

from xdg_base_dirs import xdg_config_home

LOGGER = logging.getLogger(__name__)


def get_settings():
    """
    Gets the settings
    """
    LOGGER.debug("Loading settings")
    # Default settings
    LOGGER.debug("Loading default settings")
    path = Path(__file__).parent.parent.resolve() / "settings.json"
    curr_settings = {}
    with open(path, "r", encoding="utf-8") as fh:
        curr_settings.update(json.load(fh))
    # XDG Config Dir
    path = xdg_config_home() / "virtiac" / "settings.json"
    if isfile(path):
        LOGGER.debug("Loading user settings")
        with open(path, "r", encoding="utf-8") as fh:
            curr_settings.update(json.load(fh))
    return curr_settings
