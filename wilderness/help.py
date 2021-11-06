# -*- coding: utf-8 -*-

"""Help command

"""

import argparse
import subprocess
import sys

from .command import Command


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

    def run(self) -> int:
        cmd = self.get_argument("command")
        if not self._have_man():
            print("Error: man command not available.", file=sys.stderr)
            return 1

        assert self.application
        app_name = self.application.name
        if cmd is None:
            cp = subprocess.run(["man", f"{app_name}"])
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
