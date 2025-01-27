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


@registry.register("list")
class ListCommand:
    """
    Lists domains
    """

    def __call__(self, arguments):
        """
        Lists LibVirt's domains
        """
        settings = get_settings()
        LOGGER.debug("Connecting to %s via LibVirt", settings["url"])
        conn = get_connection(settings["url"], "rw")
        LOGGER.debug("Searching for domains")
        domains = [
            item.name()
            for item in conn.listAllDomains()
        ]
        for item in domains:
            print(item)

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "list", help="Lists LibVirt's Domains"
        )
        parser.set_defaults(command="list")
