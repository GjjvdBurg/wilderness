# -*- coding: utf-8 -*-

"""ArgumentParser override

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.

"""

import argparse
import sys

from typing import TYPE_CHECKING
from typing import Optional

if TYPE_CHECKING:
    import wilderness.command


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, exit_on_error=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.exit_on_error = exit_on_error
        self._exit_called = False

    def exit(self, status: Optional[int] = 0, message: Optional[str] = None):
        if message:
            self._print_message(message, sys.stderr)
        self._exit_called = True
        if self.exit_on_error:
            sys.exit(status)


class ArgumentGroup:
    def __init__(self, group: argparse._ArgumentGroup):
        self._group = group
        self._command: Optional[wilderness.command.Command] = None

    @property
    def command(self) -> Optional["wilderness.command.Command"]:
        return self._command

    @command.setter
    def command(self, command: "wilderness.command.Command"):
        self._command = command

    def add_argument(self, *args, **kwargs):
        assert not self.command is None
        description = kwargs.pop("description", None)
        action = self._group.add_argument(*args, **kwargs)
        self.command.argument_help[action.dest] = description
        return action


class MutuallyExclusiveGroup:
    def __init__(self, meg: argparse._MutuallyExclusiveGroup):
        self._meg = meg
        self._command: Optional[wilderness.command.Command] = None

    @property
    def command(self) -> Optional["wilderness.command.Command"]:
        return self._command

    @command.setter
    def command(self, command: "wilderness.command.Command"):
        self._command = command

    def add_argument(self, *args, **kwargs):
        assert not self.command is None
        description = kwargs.pop("description", None)
        action = self._meg.add_argument(*args, **kwargs)
        self.command.argument_help[action.dest] = description
        return action
