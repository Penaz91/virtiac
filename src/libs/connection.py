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
    """
    Tries to connect to LibVirt
    """
    connection = None
    if mode == "r":
        LOGGER.debug("Connecting to %s in readonly mode", url)
        try:
            connection = libvirt.openReadOnly(url)
        except libvirt.libvirtError:
            LOGGER.fatal("Unable to open a connection to %s", url)
        return connection
    if mode == "rw":
        LOGGER.debug("Connecting to %s in read/write mode", url)
        try:
            connection = libvirt.open(url)
        except libvirt.libvirtError:
            LOGGER.fatal("Unable to open a connection to %s", url)
        return connection
    LOGGER.fatal("Invalid connection mode detected")
    return connection
