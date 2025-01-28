"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-28

Author: Penaz
"""
import logging

import libvirt

LOGGER = logging.getLogger(__name__)


def get_ips(domain):
    """
    Get the IP addresses for the domain
    """
    LOGGER.debug("Querying IP addresses for domain")
    addresses = {
        "ipv4": [],
        "ipv6": [],
    }
    networks = domain.interfaceAddresses(
        libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_ARP, 0
    )
    for netname, net in networks.items():
        if net["addrs"]:
            for ipaddr in net["addrs"]:
                if ipaddr["type"] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                    addresses["ipv4"].append(ipaddr["addr"])
                if ipaddr["type"] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                    addresses["ipv6"].append(ipaddr["addr"])
    return addresses


def start_network(conn: libvirt.virConnect, network_name: str):
    """
    Starts a network, if not already started
    """
    try:
        network = conn.networkLookupByName(network_name)
    except libvirt.libvirtError:
        LOGGER.error("Network %s does not exist", network_name)
        return
    if network.isActive():
        LOGGER.debug("Network %s already active", network_name)
        return
    network.create()
