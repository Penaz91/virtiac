"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-27

Author: Penaz
"""
import logging
from time import sleep
from uuid import uuid4

from libvirt import libvirtError

from libs import templates
from libs.disks import create_disk
from libs.forward import clean_ports, forward_ports
from libs.network import start_network

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
        new_domain(conn, domain_name, machine_settings["machines"][domain_name])
        LOGGER.info("Domain %s does not exist", domain_name)
        return
    LOGGER.info("Domain %s found", domain_name)
    LOGGER.info("Starting Domain %s", domain_name)
    # TODO: [Penaz] [2025-01-27] Check for domain existence, if doesn't
    # ^ exist, create it
    if domain.isActive():
        LOGGER.info("Domain %s already started", domain_name)
        return
    if machine_settings:
        network_name = machine_settings["machines"][domain_name]["bridge"].get(
            "net_name", "default"
        )
    else:
        network_name = "default"
    start_network(conn, network_name)
    domain.create()
    LOGGER.info("Domain %s started", domain_name)
    # TODO: [Penaz] [2025-01-28] Needs to wait for machine to be up
    if machine_settings:
        key = machine_settings["machines"][domain_name].get("key", None)
        forward_ports(machine_settings, domain, key)


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
    LOGGER.info("Waiting for domain %s to stop", domain_name)
    timer = 0
    while domain.isActive() and timer < 30:
        sleep(1)
        timer += 1
    if timer >= 30:
        LOGGER.info("Domain %s not stopping, destroying it", domain_name)
        domain.destroy()
    LOGGER.info("Domain %s stopped", domain_name)
    LOGGER.info("Cleaning forwarded ports")
    clean_ports(domain_name)


def new_domain(conn, domain_name, machine_settings):
    """
    Creates a new domain, given the settings
    """
    LOGGER.info("Creating new domain %s", domain_name)
    disks = []
    shares = []
    for idx, disk in enumerate(machine_settings["disks"]):
        create_disk(disk)
        disks.append(
            templates.DISK_TEMPLATE.format(
                format=disk["format"],
                path=disk["path"],
                dev=f"vd{chr(ord('a') + idx)}"
            )
        )
    memory_xml = templates.MEMORY_TEMPLATE.format(
        size=machine_settings["memory"].get("size", 2),
        accessmode=machine_settings["memory"].get("access_mode", "shared")
    )
    cpu_xml = templates.CPU_TEMPLATE.format(
        vcpus=machine_settings["cpu"].get("vcpus", 2),
        mode=machine_settings["cpu"].get("model", "host-model"),
        check=machine_settings["cpu"].get("check", "partial"),
    )
    interface_xml = templates.INTERFACE_TEMPLATE.format(
        network=machine_settings["bridge"].get("net_name", "default"),
        type=machine_settings["bridge"].get("type", "virtio")
    )
    for share in machine_settings["shares"]:
        shares.append(
            templates.FS_TEMPLATE.format(
                driver=share.get("driver", "virtiofs"),
                source=share["source"],
                target_name=share["target"]
            )
        )
    domain_xml = templates.DOMAIN_TEMPLATE.format(
        name=domain_name,
        uuid=str(uuid4()),
        title=machine_settings.get("title", domain_name),
        memory=memory_xml,
        cpu=cpu_xml,
        disks="".join(disks),
        shares="".join(shares),
        interface=interface_xml

    )
    conn.defineXML(domain_xml)
