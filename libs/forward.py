"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-28

Author: Penaz
"""
import logging
from subprocess import Popen

LOGGER = logging.getLogger(__name__)


def forward_port(guest_port, host_port, guest_ip, user):
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
