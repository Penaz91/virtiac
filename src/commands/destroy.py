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


@registry.register("destroy")
class DestroyCommand:
    """
    Destroy a domain
    """

    def __call__(self, arguments):
        """
        Destroys a libVirt Domain
        """
        settings = get_settings()
        domain_names = arguments.domain
        machine_settings = None
        if not domain_names:
            machine_settings = get_machine_file()
            domain_names = list(machine_settings["machines"])
        LOGGER.debug("Connecting to %s via LibVirt", settings["url"])
        conn = get_connection(settings["url"], "rw")
        LOGGER.debug("Destroying domains")
        for item in domain_names:
            confirm = ""
            while confirm.upper() not in ("Y", "N"):
                confirm = input(
                    "Do you really want to destroy the domain named %s [y/n]? "
                    % item
                )
            if confirm.upper() == "Y":
                domain = get_domain_by_name(conn, item)
                if domain is not None:
                    LOGGER.debug("Destorying domain %s", item)
                    domain.undefine()
        conn.close()

    @staticmethod
    def register_parser_subcommands(subparsers):
        """
        Registers the argument subparser
        """
        parser = subparsers.add_parser(
            "destroy", help="Destroys domains"
        )
        parser.set_defaults(command="destroy")
        parser.add_argument(
            "--domain",
            action="append",
            help="Name of the domain (if absent will find them in the "
                 "closest virtiac.json)"
        )
