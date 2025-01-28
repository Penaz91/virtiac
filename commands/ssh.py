"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-28

Author: Penaz
"""
import logging
from os import execlp, getlogin

from libs.commands import registry
from libs.connection import get_connection
from libs.domains import get_domain_by_name
from libs.files import get_machine_file
from libs.settings import get_settings

LOGGER = logging.getLogger(__name__)


@registry.register("ssh")
class SSHCommand:
    """
    Connects to a domain via SSH
    """

    def __call__(self, arguments):
        """
        Checks if a domain is started, then connects to it via SSH
        """
        settings = get_settings()
        domain_name = arguments.domain
        if not domain_name:
            machine_settings = get_machine_file()
            # TODO: [Penaz] [2025-01-28] Eventually change to support
            # ^ a different URL per machine
            domain_names = list(machine_settings["machines"])
            # TODO: [Penaz] [2025-01-28] Show an SSH selection menu
            domain_name = domain_names[0]
            machine = machine_settings["machines"][domain_name]
        LOGGER.debug("Connecting to %s via LibVirt", settings["url"])
        conn = get_connection(settings["url"], "rw")
        if not conn:
            return
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
        if not domain.isActive():
            LOGGER.info("Domain %s not started", domain_name)
            return
        LOGGER.debug("Querying ARP tables for domain IP")
        networks = domain.interfaceAddresses(2)
        for netname, net in networks.items():
            LOGGER.debug("Exploring network %s", netname)
            LOGGER.debug("Found addresses %s", net["addrs"])
            address = net["addrs"][0]["addr"]
            LOGGER.info("Connecting to %s via SSH", address)
            user = getlogin()
            if "user" in machine:
                user = machine["user"]
            ssh_command = [
                "ssh",
                "ssh",
                "-o",
                "StrictHostKeyChecking=no",
                "-o",
                "UserKnownHostsFile=/dev/null",
                f"{user}@{address}"
            ]
            if "key" in machine:
                ssh_command.extend([
                    "-i",
                    f"{machine["key"]}"
                ])
            execlp(*ssh_command)

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "ssh", help="Connects to a domain via SSH"
        )
        parser.set_defaults(command="ssh")
        parser.add_argument(
            "--domain",
            action="append",
            help="Name of the domain (if absent will find it in the "
                 "closest virtiac.json)"
        )
