"""
This file is part of the VirtIAC Project.
Copyright © 2025-2025, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2025-01-27

Author: Penaz
"""
import logging

from libs.commands import registry
from libs.connection import get_connection
from libs.domains import get_domain_by_name
from libs.files import get_machine_file, set_state
from libs.forward import forward_port
from libs.settings import get_settings

LOGGER = logging.getLogger(__name__)


@registry.register("up")
class StartCommand:
    """
    Starts a domain
    """

    def __call__(self, arguments):
        """
        Starts a domain, if it's not started already
        """
        settings = get_settings()
        domain_names = arguments.domain
        machine_settings = None
        if not domain_names:
            machine_settings = get_machine_file()
            # TODO: [Penaz] [2025-01-28] Eventually change to support
            # ^ a different URL per machine
            domain_names = list(machine_settings["machines"])
        LOGGER.debug("Connecting to %s via LibVirt", settings["url"])
        conn = get_connection(settings["url"], "rw")
        if not conn:
            return
        for domain_name in domain_names:
            LOGGER.debug(
                "Checking for existence of domain %s",
                domain_name
            )
            domain = get_domain_by_name(conn, domain_name)
            if not domain:
                LOGGER.info("Domain %s does not exist", domain_name)
                continue
            LOGGER.info("Domain %s found", domain_name)
            LOGGER.info("Starting Domain %s", domain_name)
            # TODO: [Penaz] [2025-01-27] Check for domain existence, if doesn't
            # ^ exist, create it
            if domain.isActive():
                LOGGER.info("Domain %s already started", domain_name)
                continue
            domain.create()
            LOGGER.info("Domain %s started", domain_name)
            # TODO: [Penaz] [2025-01-28] Needs to wait for machine to be up
            if machine_settings:
                if "forwarded_ports" in machine_settings["machines"][domain_name]:
                    for port_dict in machine_settings["machines"][domain_name]["forwarded_ports"]:
                        pid = forward_port(
                            port_dict["guest"],
                            port_dict["host"],
                            # XXX: [Penaz] [2025-01-28] Temporary
                            "192.168.121.19",
                            "vagrant"
                        )
                        set_state(
                            domain_name, "forwarded_ports_pids", pid, True
                        )

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "up", help="Starts a domain"
        )
        parser.set_defaults(command="up")
        parser.add_argument(
            "--domain",
            action="append",
            help="Name of the domain (if absent will find it in the "
                 "closest virtiac.json)"
        )
