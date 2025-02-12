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
from libs.domains import start_domain, stop_domain
from libs.files import get_machine_file
from libs.settings import get_settings

LOGGER = logging.getLogger(__name__)


@registry.register("reload")
class ReloadCommand:
    """
    Reloads a domain
    """

    def __call__(self, arguments):
        """
        Restarts a domain, if it's started
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
            LOGGER.info("Restarting domain %s", domain_name)
            stop_domain(conn, domain_name)
            start_domain(conn, domain_name, machine_settings)
        conn.close()

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "reload", help="Shuts down and restarts a domain"
        )
        parser.set_defaults(command="reload")
        parser.add_argument(
            "--domain",
            action="append",
            help="Name of the domain (if absent will find it in the "
                 "closest virtiac.json)"
        )
