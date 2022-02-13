# -*- coding: utf-8 -*-

"""Command definition

This module contains the definitions for the Command class.

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.
"""

import abc
import argparse

from typing import TYPE_CHECKING
from typing import Dict
from typing import Optional

from .documentable import DocumentableMixin
from .manpages import ManPage

if TYPE_CHECKING:
    from .application import Application


class Command(DocumentableMixin, metaclass=abc.ABCMeta):
    def __init__(
        self,
        name: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        add_help: Optional[bool] = True,
        extra_sections: Optional[Dict[str, str]] = None,
        options_prolog: Optional[str] = None,
        options_epilog: Optional[str] = None,
    ):
        super().__init__(
            description=description,
            extra_sections=extra_sections,
            options_prolog=options_prolog,
            options_epilog=options_epilog,
        )
        self._name = name
        self._title = title

        self._args = None  # type: Optional[argparse.Namespace]
        self._application = None  # type: Optional[Application]
        self._add_help = add_help

    @property
    def application(self) -> Optional["Application"]:
        return self._application

    @property
    def args(self) -> argparse.Namespace:
        assert self._args is not None
        return self._args

    @property
    def name(self) -> str:
        return self._name

    @property
    def title(self) -> Optional[str]:
        return self._title

    def add_argument(self, *args, **kwargs):
        assert self._parser is not None
        description = kwargs.pop("description", None)
        action = self._parser.add_argument(*args, **kwargs)
        self._arg_help[action.dest] = description
        return action

    def add_mutually_exclusive_group(
        self, *args, **kwargs
    ) -> argparse._MutuallyExclusiveGroup:
        assert self._parser is not None
        group = self._parser.add_mutually_exclusive_group(*args, **kwargs)
        return group

    def set_parser(self, parser: argparse.ArgumentParser):
        self._parser = parser

    def set_args(self, args: argparse.Namespace):
        self._args = args

    def register(self):
        pass

    @abc.abstractmethod
    def handle(self) -> int:
        pass

    def create_manpage(self) -> ManPage:
        assert self.application is not None
        man = ManPage(
            self.application.name,
            command_name=self.name,
            version=self.application.version,
            title=self._title,
            author=self.application.author,
        )
        self.populate_manpage(man)
        return man
