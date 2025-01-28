"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-28

Author: Penaz
"""
import logging
import signal
from os import kill
from subprocess import Popen

from libs.files import get_state, set_state

LOGGER = logging.getLogger(__name__)


def forward_single_port(guest_port, host_port, guest_ip, user):
    """
    Forwards a guest port to the host via SSH, returning the process PID
    """
    LOGGER.info(
        "Forwarding guest port %s to host port %s", guest_port, host_port
    )
    command = [
        "ssh",
        "-L",
        f"*:{host_port}:{guest_ip}:{guest_port}",
        "-N",
        f"{user}@{guest_ip}"
    ]
    process = Popen(command)
    return process.pid


def forward_ports(domain_settings, domain_name):
    """
    Forward all defined ports in the virtiac.json file
    """
    if "forwarded_ports" in domain_settings["machines"][domain_name]:
        for port_dict in domain_settings["machines"][domain_name]["forwarded_ports"]:
            pid = forward_single_port(
                port_dict["guest"],
                port_dict["host"],
                # XXX: [Penaz] [2025-01-28] Temporary
                "192.168.121.19",
                "vagrant"
            )
            set_state(
                domain_name, "forwarded_ports_pids", pid, True
            )


def clean_ports(domain_name):
    """
    Kills all port forwarding SSH connections
    """
    state = get_state()
    if domain_name in state["machines"]:
        if "forwarded_ports_pids" in state["machines"][domain_name]:
            for pid in state["machines"][domain_name]["forwarded_ports_pids"]:
                try:
                    kill(pid, signal.SIGTERM)
                except ProcessLookupError:
                    LOGGER.debug("Process with pid %s not found", pid)
                    continue
            set_state(
                domain_name, "forwarded_ports_pids", []
            )
