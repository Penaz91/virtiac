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
from libs.settings import get_settings

LOGGER = logging.getLogger(__name__)


@registry.register("check")
class CheckCommand:
    """
    Checks if a domain exists
    """

    def __call__(self, arguments):
        """
        Checks if a domain exists and returns a result
        """
        settings = get_settings()
        domain_names = arguments.domain
        if not domain_names:
            machine_settings = get_machine_file()
            # TODO: [Penaz] [2025-01-28] Eventually change to support
            # ^ a different URL per machine
            domain_names = [
                item["name"]
                for item in machine_settings["machines"]
            ]
        LOGGER.debug("Connecting to %s via LibVirt", settings["url"])
        conn = get_connection(settings["url"])
        if not conn:
            return
        for domain_name in domain_names:
            LOGGER.debug(
                "Checking for existence of domain %s", domain_name
            )
            domain = get_domain_by_name(conn, domain_name)
            if domain:
                LOGGER.info("Domain %s Found", domain_name)

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "check", help="Checks for the existence of a domain"
        )
        parser.set_defaults(command="check")
        parser.add_argument(
            "--domain",
            help="Name of the domain (if absent will find it in the "
                 "closest virtiac.json)"
        )
