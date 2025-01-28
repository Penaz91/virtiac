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
from libs.files import get_machine_file
from libs.forward import clean_ports
from libs.settings import get_settings

LOGGER = logging.getLogger(__name__)


@registry.register("halt")
class HaltCommand:
    """
    Stops a domain
    """

    def __call__(self, arguments):
        """
        Stops a domain, if it's not stopped already
        """
        settings = get_settings()
        domain_names = arguments.domain
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
            LOGGER.info("Stopping Domain %s", domain_name)
            if not domain.isActive():
                LOGGER.info("Domain %s already stopped", domain_name)
                continue
            domain.shutdown()
            LOGGER.info("Domain %s stopped", domain_name)
            LOGGER.info("Cleaning forwarded ports")
            clean_ports(domain_name)
            conn.close()

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "halt", help="Stops a domain"
        )
        parser.set_defaults(command="halt")
        parser.add_argument(
            "--domain",
            help="Name of the domain (if absent will find it in the "
                 "closest virtiac.json)"
        )
