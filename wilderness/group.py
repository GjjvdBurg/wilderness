# -*- coding: utf-8 -*-

"""Group definitions

This module contains the definitions for the Group class, which is used to 
collect distinct Command objects for the application.

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.

"""

import argparse

from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Optional

if TYPE_CHECKING:
    from wilderness import Application
    from wilderness import Command


class Group:
    def __init__(self, title: Optional[str] = None):
        self._title = title

        self._command_map = {}  # type: Dict[str, Command]
        self._app = None  # type: Optional[Application]

    @property
    def application(self) -> Optional["Application"]:
        return self._app

    @property
    def title(self) -> Optional[str]:
        return self._title

    @property
    def commands(self) -> List["Command"]:
        return list(self._command_map.values())

    def commands_as_actions(self) -> List[argparse.Action]:
        actions = []
        for command in self.commands:
            action = argparse.Action(
                option_strings=[], dest=command.name, help=command.title
            )
            actions.append(action)
        return actions

    def set_app(self, app: "Application") -> None:
        self._app = app

    def add(self, command: "Command") -> None:
        self._command_map[command.name] = command
        assert self.application is not None
        self.application._add_command(command)

    def __len__(self) -> int:
        return len(self.commands)
