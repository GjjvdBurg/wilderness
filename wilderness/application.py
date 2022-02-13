# -*- coding: utf-8 -*-

"""Application class

This module contains the Application class.

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.
"""

import argparse
import sys

from typing import Dict
from typing import List
from typing import Optional

from .command import Command
from .documentable import DocumentableMixin
from .formatter import HelpFormatter
from .group import Group
from .help import HelpCommand
from .help import help_action_factory
from .manpages import ManPage
from .parser import ArgumentParser


class Application(DocumentableMixin):

    _cmd_name = "command"

    def __init__(
        self,
        name: str,
        version: str,
        author: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        default_command: Optional[str] = None,
        add_help: bool = True,
        extra_sections: Optional[Dict[str, str]] = None,
        prolog: Optional[str] = None,
        epilog: Optional[str] = None,
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
        self._version = version
        self._author = "" if author is None else author
        self._title = title
        self._default_command = default_command
        self._add_help = add_help

        self._parser = ArgumentParser(
            prog=name,
            description=prolog,
            epilog=epilog,
            formatter_class=HelpFormatter,
            add_help=False,
        )  # type: ArgumentParser
        self._subparsers = None  # type: Optional[argparse._SubParsersAction]

        self._command_map = {}  # type: Dict[str, Command]
        self._group_map = {}  # type: Dict[str, Group]
        self._root_group = None  # type: Optional[Group]
        self._args = None  # type: Optional[argparse.Namespace]

        self._prolog = prolog
        self._epilog = epilog

        default_prefix = "-"  # TODO: allow the user to set this and extract from self._parser
        if self._add_help:
            self._parser.add_argument(
                default_prefix + "h",
                default_prefix * 2 + "help",
                action=help_action_factory(self),
                default=argparse.SUPPRESS,
                help="show this help message and exit",
            )
            self.add(HelpCommand())

        self.register()

    @property
    def name(self) -> str:
        """The name of the application"""
        return self._name

    @property
    def author(self) -> str:
        """The author(s) of the application"""
        return self._author

    @property
    def version(self) -> str:
        """The version of the package or application"""
        return self._version

    @property
    def args(self) -> argparse.Namespace:
        """The parsed command line arguments"""
        assert self._args is not None
        return self._args

    @property
    def commands(self) -> List[Command]:
        """List the commands registered to the application"""
        cmds = []
        if self._root_group:
            cmds.extend(list(self._root_group.commands))
        for group in self._group_map.values():
            cmds.extend(list(group.commands))
        return cmds

    def add_argument(self, *args, **kwargs) -> argparse.Action:
        """Add an argument to the application

        This wraps the argparse.ArgumentParser.add_argument method, with the
        minor difference that it supports a "description" keyword argument,
        which will be used to provide a long help message for the argument in
        the man page.
        """
        help_ = kwargs.get("help", None)
        description = kwargs.pop("description", help_)
        action = self._parser.add_argument(*args, **kwargs)
        self._arg_help[action.dest] = description
        return action

    def add_mutually_exclusive_group(
        self, *args, **kwargs
    ) -> argparse._MutuallyExclusiveGroup:
        assert self._parser is not None
        group = self._parser.add_mutually_exclusive_group(*args, **kwargs)
        return group

    def add(self, command: Command):
        if self._subparsers is None:
            self._subparsers = self._parser.add_subparsers(
                dest="target", metavar=self._cmd_name
            )
        if self._root_group is None:
            self._root_group = Group(title="Available commands")
            self._root_group.set_app(self)
        self._root_group.add(command)

    def _add_command(self, command: Command):
        assert self._subparsers is not None
        self._command_map[command._name] = command
        cmd_parser = self._subparsers.add_parser(
            command.name,
            help=command.title,
            add_help=command._add_help,
        )
        command.set_parser(cmd_parser)
        command.register()
        command._application = self

    def add_group(self, title: str) -> Group:
        group = Group(title)
        group.set_app(self)
        self._group_map[title] = group
        return group

    def register(self):
        pass

    def handle(self) -> int:
        return 1

    def run(
        self,
        args: Optional[List[str]] = None,
        namespace: Optional[argparse.Namespace] = None,
        exit_on_error: Optional[bool] = True,
    ) -> int:
        self._parser.exit_on_error = exit_on_error
        parsed_args = self._parser.parse_args(args=args, namespace=namespace)
        self.set_args(parsed_args)
        if self._subparsers is None:
            return self.handle()

        assert self.args is not None

        if self.args.target is None:
            if self._default_command:
                self.args.target = self._default_command
            else:
                self.print_help()
                return 1

        command = self.get_command(self.args.target)
        command.set_args(self.args)
        return self.run_command(command)

    def run_command(self, command: Command) -> int:
        # This is here so the user can override how commands are executed
        return command.handle()

    def get_command(self, cmd_name: str) -> Command:
        return self._command_map[cmd_name]

    def set_args(self, args: argparse.Namespace) -> None:
        self._args = args

    def set_prolog(self, prolog: str) -> None:
        self._prolog = prolog

    def set_epilog(self, epilog: str) -> None:
        self._epilog = epilog

    def create_manpage(self) -> ManPage:
        man = ManPage(
            self.name,
            version=self._version,
            title=self._title,
            author=self._author,
        )
        self.populate_manpage(man)
        return man

    def format_help(self) -> str:
        formatter = argparse.RawTextHelpFormatter(prog=self._parser.prog)

        # usage
        formatter.add_usage(
            self._parser.usage,
            self._parser._actions,
            self._parser._mutually_exclusive_groups,
        )

        # prolog
        formatter.add_text(self._prolog)

        # add commands from root group, unless we only have help
        only_help = (
            self._root_group
            and len(self._root_group) == 1
            and self._root_group.commands[0].name == "help"
        )
        if self._root_group and not only_help:
            formatter.start_section(self._root_group.title)
            actions = self._root_group.commands_as_actions()
            formatter.add_arguments(actions)
            formatter.end_section()

        # add commands from other groups
        for group in self._group_map.values():
            formatter.start_section(group.title)
            actions = group.commands_as_actions()
            formatter.add_arguments(actions)
            formatter.end_section()

        # epilog
        formatter.add_text(self._epilog)

        # determine help from format above
        return formatter.format_help()

    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        message = self.format_help()
        self._parser._print_message(message, file=file)
