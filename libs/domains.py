"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-27

Author: Penaz
"""
import logging

from libvirt import libvirtError

LOGGER = logging.getLogger(__name__)


def get_domain_by_name(connection, name):
    """
    Tries to get a domain, given its internal name
    """
    domain = None
    try:
        domain = connection.lookupByName(name)
    except libvirtError:
        LOGGER.error("Unable to find domain %s", name)
    return domain
