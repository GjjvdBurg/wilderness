# -*- coding: utf-8 -*-

"""Command class

"""

import abc
import argparse

from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import Optional

from .documentable import DocumentableMixin
from .manpages import ManPage

if TYPE_CHECKING:
    from .application import Application


class Command(DocumentableMixin, metaclass=abc.ABCMeta):
    def __init__(
        self,
        name: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        extra_sections: Optional[Dict[str, str]] = None,
        add_help: Optional[bool] = True,
    ):
        self._name = name
        self._title = title
        self._description = description
        self._extra_sections = {} if extra_sections is None else extra_sections

        self._parser = None  # type: argparse.ArgumentParser
        self._args = None  # type: argparse.Namespace
        self._arg_help = {}

        self._application = None  # type: Optional[Application]
        self._add_help = add_help

    @property
    def application(self) -> "Application":
        return self._application

    @property
    def name(self) -> str:
        return self._name

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    def add_argument(self, *args, **kwargs):
        description = kwargs.pop("description", None)
        action = self._parser.add_argument(*args, **kwargs)
        self._arg_help[action.dest] = description
        return action

    def set_parser(self, parser: argparse.ArgumentParser):
        self._parser = parser

    def set_args(self, args: argparse.Namespace):
        self._args = args

    def get_argument(self, name: str) -> Any:
        return getattr(self._args, name)

    def register(self):
        pass

    @abc.abstractmethod
    def run(self) -> int:
        pass

    def create_manpage(self) -> ManPage:
        man = ManPage(
            self.application.name,
            command_name=self.name,
            version=self.application.version,
            title=self._title,
            author=self.application.author,
        )
        self.populate_manpage(man)
        return man
