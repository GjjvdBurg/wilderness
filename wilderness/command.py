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

from wilderness.argparse_wrappers import ArgumentGroup
from wilderness.argparse_wrappers import MutuallyExclusiveGroup
from wilderness.documentable import DocumentableMixin
from wilderness.manpages import ManPage

if TYPE_CHECKING:
    import wilderness.application


class Command(DocumentableMixin, metaclass=abc.ABCMeta):
    def __init__(
        self,
        name: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        add_help: bool = True,
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

        self._args: Optional[argparse.Namespace] = None
        self._application: Optional[wilderness.application.Application] = None
        self._add_help = add_help

    @property
    def application(self) -> Optional["wilderness.application.Application"]:
        return self._application

    @property
    def name(self) -> str:
        return self._name

    @property
    def title(self) -> Optional[str]:
        return self._title

    def add_argument(self, *args, **kwargs):
        assert self._parser is not None
        help_ = kwargs.get("help", None)
        description = kwargs.pop("description", help_)
        action = self._parser.add_argument(*args, **kwargs)
        self._arg_help[action.dest] = description
        return action

    def add_argument_group(self, *args, **kwargs) -> ArgumentGroup:
        assert self._parser is not None
        _group = self._parser.add_argument_group(*args, **kwargs)
        group = ArgumentGroup(_group)
        group.command = self
        return group

    def add_mutually_exclusive_group(
        self, *args, **kwargs
    ) -> MutuallyExclusiveGroup:
        assert self._parser is not None
        _meg = self._parser.add_mutually_exclusive_group(*args, **kwargs)
        meg = MutuallyExclusiveGroup(_meg)
        meg.command = self
        return meg

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
        man.add_section_synopsis(self.get_synopsis())
        if self.description:
            man.add_section("description", self.description)
        man.add_section("options", self.get_options_text())
        for sec in self._extra_sections:
            man.add_section(sec, self._extra_sections[sec])
        return man
