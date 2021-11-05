# -*- coding: utf-8 -*-

"""Application class

"""

import argparse
import sys

from typing import Dict
from typing import List
from typing import Optional

from .command import Command
from .documentable import DocumentableMixin
from .group import Group
from .formatter import HelpFormatter
from .help import HelpCommand
from .manpages import ManPage


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
        header: Optional[str] = None,
        footer: Optional[str] = None,
    ):
        self._name = name
        self._version = version
        self._author = "" if author is None else author
        self._title = title
        self._description = description
        self._default_command = default_command

        self._parser = argparse.ArgumentParser(
            prog=name, formatter_class=HelpFormatter
        )
        self._subparsers = self._parser.add_subparsers(
            dest="target", metavar=self._cmd_name
        )

        self._command_map = {}
        self._group_map = {}
        self._root_group = None
        self._arg_help = {}

        self._extra_sections = {} if extra_sections is None else extra_sections
        self._header = header
        self._footer = footer

        if add_help:
            self.add(HelpCommand())

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def author(self) -> str:
        return self._author

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def commands(self) -> List[Command]:
        cmds = []
        if self._root_group:
            cmds.extend(list(self._root_group.commands))
        for group in self._group_map.values():
            cmds.extend(list(group.commands))
        return cmds

    def add_argument(self, *args, **kwargs) -> argparse.Action:
        description = kwargs.pop("description", None)
        action = self._parser.add_argument(*args, **kwargs)
        self._arg_help[action.dest] = description
        return action

    def add(self, command: Command):
        if self._root_group is None:
            self._root_group = Group(title="")
            self._root_group.set_app(self)
        self._root_group.add(command)

    def _add_command(self, command: Command):
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

    def run(self):
        args = self._parser.parse_args()
        if args.target is None:
            if self._default_command:
                args.target = self._default_command
            else:
                return self.print_help()

        self._command_map[args.target].set_args(args)
        self._command_map[args.target].run()

    def get_command(self, cmd_name: str) -> Optional[Command]:
        return self._command_map.get(cmd_name)

    def set_header(self, header: str) -> None:
        self._header = header

    def set_footer(self, footer: str) -> None:
        self._footer = footer

    def create_manpage(self) -> ManPage:
        man = ManPage(
            self.name,
            version=self._version,
            title=self._title,
            author=self._author,
        )
        self.populate_manpage(man)
        return man

    def format_help(self):
        #formatter = self._parser._get_formatter()
        formatter = argparse.RawTextHelpFormatter(prog=self._parser.prog)

        # usage
        formatter.add_usage(
            self._parser.usage,
            self._parser._actions,
            self._parser._mutually_exclusive_groups,
        )

        # header
        formatter.add_text(self._header)

        # add commands from root group
        for group in self._group_map.values():
            formatter.start_section(group.title)
            actions = group.commands_as_actions()
            formatter.add_arguments(actions)
            formatter.end_section()

        # footer
        formatter.add_text(self._footer)

        # determine help from format above
        return formatter.format_help()

    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        message = self.format_help()
        self._parser._print_message(message, file=file)
