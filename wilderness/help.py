# -*- coding: utf-8 -*-

"""Help command definitions

This module contains the definitions for our HelpCommand and our HelpAction.  
The HelpCommand takes care of opening the manpage when the "help" subcommand is 
called, and the HelpAction is slightly modified to use our help text formatter 
(see the Application class).

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.
"""

import argparse
import subprocess
import sys

from typing import TYPE_CHECKING

from .command import Command

if TYPE_CHECKING:
    import wilderness.application


class HelpCommand(Command):
    def __init__(self):
        super().__init__(
            name="help",
            title="Display help information",
            description="Display help information",
        )

    def handle(self) -> int:
        assert self.args is not None
        assert self.application

        cmd = self.args.command
        if cmd is None:
            self.application.print_help()
            return 1

        if not have_man_command():
            print("Error: man command not available.", file=sys.stderr)
            return 2

        app_name = self.application.name
        cp = subprocess.run(["man", f"{app_name}-{cmd}"])
        return cp.returncode

    def register(self):
        self.add_argument(
            "command",
            nargs="?",
            # help=argparse.SUPPRESS,
            description=argparse.SUPPRESS,
        )


def help_action_factory(app: "wilderness.application.Application"):
    class HelpAction(argparse.Action):
        _app = app

        def __init__(
            self,
            option_strings,
            dest=argparse.SUPPRESS,
            default=argparse.SUPPRESS,
            help=None,
        ):
            super().__init__(
                option_strings=option_strings,
                dest=dest,
                default=default,
                nargs=0,
                help=help,
            )

        def __call__(self, parser, namespace, values, option_string=None):
            if self._app is None:
                parser.print_help()
            else:
                self._app.print_help()
            parser.exit()

    return HelpAction


def have_man_command() -> bool:
    try:
        cp = subprocess.run(
            ["man", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return False
    return cp.returncode == 0
