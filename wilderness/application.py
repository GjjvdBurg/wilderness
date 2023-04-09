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
from typing import TextIO

from wilderness.argparse_wrappers import ArgumentParser
from wilderness.command import Command
from wilderness.documentable import DocumentableMixin
from wilderness.formatter import HelpFormatter
from wilderness.group import Group
from wilderness.help import HelpCommand
from wilderness.help import help_action_factory
from wilderness.manpages import ManPage


class Application(DocumentableMixin):
    """Base class for applications

    .. _FakeDF: https://github.com/GjjvdBurg/wilderness/tree/master/examples/fakedf

    This is the main Application object that Wilderness applications are
    expected to inherit from. All text that is supplied to the man pages, such
    as the description, can use basic formatting constructs documented in the
    :obj:`ManPage.groffify() <wilderness.manpages.ManPage.groffify>` method.

    Parameters
    ----------
    name : str
        The name of the application.

    version : str
        The version of the application, to be used in creating the man pages.

    author : Optional[str]
        The author(s) of the application. This is used in the man pages, but is
        not actually visible in the output (it is recorded in the metadata
        header of the man pages).

    title : Optional[str]
        The title of the application is used as a short description. It shows
        up in the man pages as the text after the application name in the first
        section.

    description : Optional[str]
        Long description of the application. This is used in the man pages in
        the DESCRIPTION section after the synopsis.

    default_command : Optional[str]
        The default command to run when none is supplied on the command line.
        By default this is omitted and the help text is shown instead, but some
        applications may want to run a particular command as default instead.

    add_help : bool
        Whether to add help commands or not. This adds support for the
        traditional help flags ``-h`` or ``--help`` for the short help text on
        the command line, as well as the ``help`` command that opens the man
        pages for the subcommands of the application. Note that the short help
        text on the command line typically provides a list of available
        commands.

        See the `FakeDF`_ example for an application where this is not
        enabled.

    extra_sections : Optional[Dict[str, str]]
        Additional sections of documentation for the man page. This is expected
        to be provided as a dictionary where the keys are the section headers
        and the values are the section text. Basic formatting constructs such
        as lists and enumerations are understood by the text processor (see
        :obj:`ManPage.groffify() <wilderness.manpages.ManPage.groffify>` for
        further details).

    prolog : Optional[str]
        Text to be shown in the short command line help text, before the
        (grouped) list of available commands. Newline characters are preserved.

    epilog: Optional[str]
        Text to be shown in the short command line help text, after the list of
        available commands. Newline characters are preserved.

    options_prolog: Optional[str]
        Text to be shown in the man page before the list of options. See the
        `FakeDF`_ application for an example.

    options_epilog: Optional[str]
        Text to be shown in the man page after the list of options. See the
        `FakeDF`_ application for an example.

    add_commands_section: bool
        Whether to automatically generate a section in the application man page
        that lists the available commands.


    """

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
        add_commands_section: bool = False,
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

        self._add_commands_section = add_commands_section

        # TODO: allow the user to set this and extract from self._parser
        default_prefix = "-"
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
    def commands(self) -> List[Command]:
        """List the commands registered to the application

        Returns
        -------
        commands : List[:class:`wilderness.command.Command`]
            The list of commands registered to the application.

        """
        cmds = []
        if self._root_group:
            cmds.extend(list(self._root_group.commands))
        for group in self._group_map.values():
            cmds.extend(list(group.commands))
        return cmds

    @property
    def groups(self) -> List[Group]:
        """List the groups registered to the application

        If no groups have been added to the application but commands have been
        added, this property will contain a single group, the root group.

        Returns
        -------
        groups: List[:class:`wilderness.group.Group`]
            The list of groups registered to the application

        """
        groups = []
        if self._root_group is not None:
            groups.append(self._root_group)
        for group in self._group_map.values():
            groups.append(group)
        return groups

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

    def add(self, command: Command):
        """Add a command to the application

        Note that the ``register`` method of the command is called when it is
        added to the application.

        Parameters
        ----------
        command : :class:`wilderness.command.Command`
            The command to add to the application.

        """
        if self._subparsers is None:
            self._subparsers = self._parser.add_subparsers(
                dest="target", metavar=self._cmd_name
            )
        if self._root_group is None:
            self._root_group = Group(title="Available commands", is_root=True)
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
        command.parser = cmd_parser
        command.register()
        command._application = self

    def add_group(self, title: str) -> Group:
        """Create a group of commands

        Parameters
        ----------
        title : str
            The title for the group.

        Returns
        -------
        :class:`wilderness.group.Group`
            The created command group.

        """
        group = Group(title)
        group.set_app(self)
        self._group_map[title] = group
        return group

    def register(self):
        """Register arguments to the application

        Override this method to add command line arguments to the application
        (using self.add_argument, etc). For single-command applications, this
        should be used to add all command line arguments. For multi-command
        applications, this method can be used to add arguments that apply to
        all commands, or arguments such as --version.

        This method is called upon initialization of the Application object.

        """
        pass

    def handle(self) -> int:
        """Main method to override for single-command applications.

        When creating a single-command application (such as the `FakeDF`_
        example), this method must be overridden with the actual functionality.
        For multi-command applications, this method is not used.

        Returns
        -------
        return_code : int
            The return code of the application, to be used as the return code
            on the command line.

        """
        return 1

    def run(
        self,
        args: Optional[List[str]] = None,
        namespace: Optional[argparse.Namespace] = None,
        exit_on_error: bool = True,
    ) -> int:
        """Main method to run the application

        Parameters
        ----------
        args : Optional[List[str]]
            List of arguments to the application. This is typically only used
            for testing, as by default the arguments will be read from the
            command line.

        namespace : Optional[argparse.Namespace]
            Namespace object to save the arguments to. By default a new
            argparse.Namespace object is created.

        exit_on_error : bool
            Whether or not to exit when argparse encounters an error.

        Returns
        -------
        return_code : int
            The return code of the application, to be used as the return code
            at the command line.

        """
        # Parse the command line arguments as given
        self._parser.exit_on_error = exit_on_error
        parsed_args = self._parser.parse_args(args=args, namespace=namespace)

        # If a parser error caused argparse to print the help, then we stop
        # here
        if self._parser._exit_called:
            return 1

        # If there are no subparsers registered, we have an application without
        # subcommands, so the application handles things
        self.args = parsed_args
        if self._subparsers is None:
            return self.handle()

        # Satisfy mypy
        assert self.args is not None

        # If we have no target, check if we have a default and set that as the
        # target. If we don't print help and exit.
        if self.args.target is None:
            if self._default_command:
                self.args.target = self._default_command
            else:
                self.print_help()
                return 1

        # Run the requested command
        command = self.get_command(self.args.target)
        command.args = self.args
        return self.run_command(command)

    def run_command(self, command: Command) -> int:
        """Run a particular command directy

        Parameters
        ----------
        command : :class:`wilderness.command.Command`
            The command to execute

        Returns
        -------
        return_code : int
            The return code of the handle() method of the command.

        """
        # This is here so the user can override how commands are executed
        return command.handle()

    def get_command(self, command_name: str) -> Command:
        """Get a command by name

        Parameters
        ----------
        command_name : str
            The name of the command to find

        Returns
        -------
        command : :class:`wilderness.command.Command`
            The instance of the Command to be returned.

        Raises
        ------
        KeyError
            If no command with the provided name can be found, a KeyError is
            raised.

        """
        return self._command_map[command_name]

    def set_prolog(self, prolog: str) -> None:
        """Set the prolog of the command line help text

        Parameters
        ----------
        prolog : str
            Text to include before the list of commands in the command line
            help text. The prolog is printed after the synopsis of the
            application.

        """
        self._prolog = prolog

    def set_epilog(self, epilog: str) -> None:
        """Set the epilog of the command line help text

        Parameters
        ----------
        epilog : str
            Text to include at the end of the command line help text.

        """
        self._epilog = epilog

    def get_commands_text(self) -> str:
        text = []
        for cmd in self.commands:
            text.append(f"{self.name}-{cmd.name}(1)")
            text.append(f"\t{cmd.title or ''}")
            text.append("")
        return "\n".join(text)

    def create_manpage(self) -> ManPage:
        """Create the Manpage for the application

        Returns
        -------
        man_page : :class:`wilderness.manpages.ManPage`
            The generated ManPage object.

        """
        man = ManPage(
            self.name,
            version=self._version,
            title=self._title,
            author=self._author,
        )
        man.add_section_synopsis(self.get_synopsis())
        if self.description:
            man.add_section("description", self.description)
        man.add_section("options", self.get_options_text())
        if self._add_commands_section:
            man.add_section("commands", self.get_commands_text())
        for sec in self._extra_sections:
            man.add_section(sec, self._extra_sections[sec])
        return man

    def format_help(self) -> str:
        """Format the command line help for the application

        This method creates the help text for the command line, which is
        typically printed when the -h / --help / help command line arguments
        are used. The :func:`print_help` method calls this method to format
        the help text.

        Returns
        -------
        help_text : str
            The help text as a single string.

        """
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

    def print_help(self, file: Optional[TextIO] = None):
        """Print the command line help text for the application

        Parameters
        ----------
        file : Optional[TextIO]
            The file to which to write the help text. If omitted, the help text
            will be written to sys.stdout.

        """
        if file is None:
            file = sys.stdout
        message = self.format_help()
        self._parser._print_message(message, file=file)
