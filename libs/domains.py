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

from libs.forward import clean_ports, forward_ports

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


def start_domain(conn, domain_name, machine_settings=None):
    LOGGER.debug(
        "Checking for existence of domain %s",
        domain_name
    )
    domain = get_domain_by_name(conn, domain_name)
    if not domain:
        LOGGER.info("Domain %s does not exist", domain_name)
        return
    LOGGER.info("Domain %s found", domain_name)
    LOGGER.info("Starting Domain %s", domain_name)
    # TODO: [Penaz] [2025-01-27] Check for domain existence, if doesn't
    # ^ exist, create it
    if domain.isActive():
        LOGGER.info("Domain %s already started", domain_name)
        return
    domain.create()
    LOGGER.info("Domain %s started", domain_name)
    # TODO: [Penaz] [2025-01-28] Needs to wait for machine to be up
    if machine_settings:
        forward_ports(machine_settings, domain_name)


def stop_domain(conn, domain_name):
    LOGGER.debug(
        "Checking for existence of domain %s",
        domain_name
    )
    domain = get_domain_by_name(conn, domain_name)
    if not domain:
        LOGGER.info("Domain %s does not exist", domain_name)
        return
    LOGGER.info("Domain %s found", domain_name)
    LOGGER.info("Stopping Domain %s", domain_name)
    if not domain.isActive():
        LOGGER.info("Domain %s already stopped", domain_name)
        return
    domain.shutdown()
    LOGGER.info("Domain %s stopped", domain_name)
    LOGGER.info("Cleaning forwarded ports")
    clean_ports(domain_name)
