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
    import wilderness.application
    import wilderness.command


class Group:
    def __init__(self, title: Optional[str] = None, is_root: bool = False):
        self._title = title
        self._is_root = is_root

        self._command_map: Dict[str, wilderness.command.Command] = {}
        self._app: Optional[wilderness.application.Application] = None

    @property
    def application(self) -> Optional["wilderness.application.Application"]:
        return self._app

    @property
    def title(self) -> Optional[str]:
        return self._title

    @property
    def commands(self) -> List["wilderness.command.Command"]:
        return list(self._command_map.values())

    @property
    def is_root(self) -> bool:
        """Return whether the groups is its Application's root group"""
        return self._is_root

    def commands_as_actions(self) -> List[argparse.Action]:
        actions = []
        for command in self.commands:
            action = argparse.Action(
                option_strings=[], dest=command.name, help=command.title
            )
            actions.append(action)
        return actions

    def set_app(self, app: "wilderness.application.Application") -> None:
        self._app = app

    def add(self, command: "wilderness.command.Command") -> None:
        self._command_map[command.name] = command
        assert self.application is not None
        self.application._add_command(command)

    def __len__(self) -> int:
        return len(self.commands)
