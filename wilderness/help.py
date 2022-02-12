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
    from .application import Application


class HelpCommand(Command):
    def __init__(self):
        super().__init__(
            name="help",
            title="Display help information",
            description="Display help information",
        )

    def _have_man(self) -> bool:
        try:
            cp = subprocess.run(
                ["man", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except FileNotFoundError:
            return False
        if not cp.returncode == 0:
            return False
        return True

    def handle(self) -> int:
        assert self.args is not None
        cmd = self.args.command
        if not self._have_man():
            print("Error: man command not available.", file=sys.stderr)
            return 1

        assert self.application
        app_name = self.application.name
        if cmd is None:
            self.application.print_help()
            return 1
        else:
            cp = subprocess.run(["man", f"{app_name}-{cmd}"])
        return cp.returncode

    def register(self):
        self.add_argument(
            "command",
            nargs="?",
            # help=argparse.SUPPRESS,
            description=argparse.SUPPRESS,
        )


def help_action_factory(app: "Application"):
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
