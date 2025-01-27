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
        LOGGER.debug("Connecting to %s via LibVirt", settings["url"])
        conn = get_connection(settings["url"])
        LOGGER.debug("Checking for existence of domain %s", arguments.domain)
        domain = get_domain_by_name(conn, arguments.domain)
        if domain:
            print(f"Domain {arguments.domain} Found")

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "check", help="Checks for the existence of a domain"
        )
        parser.set_defaults(command="check")
        parser.add_argument("domain", help="The domain name to search for")
