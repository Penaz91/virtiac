"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-27

Author: Penaz
"""
import logging

import libvirt

LOGGER = logging.getLogger(__name__)


def get_connection(url=None, mode="r"):
    if mode == "r":
        LOGGER.debug("Connecting to %s in readonly mode", url)
        connection = libvirt.openReadOnly(url)
        return connection
    if mode == "rw":
        LOGGER.debug("Connecting to %s in read/write mode", url)
        connection = libvirt.open(url)
        return connection
