# -*- coding: utf-8 -*-

"""DocumentableMixin definitions

A documentable is either an application or command, for which we can generate a 
manpage.

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.
"""

import abc
import argparse

from typing import Dict
from typing import Optional

from wilderness.formatter import HelpFormatter
from wilderness.manpages import ManPage


class DocumentableMixin(metaclass=abc.ABCMeta):
    def __init__(
        self,
        description: Optional[str] = None,
        extra_sections: Optional[Dict[str, str]] = None,
        options_prolog: Optional[str] = None,
        options_epilog: Optional[str] = None,
    ):
        self._description = description  # type: Optional[str]
        self._args = None  # type: Optional[argparse.Namespace]
        self._parser = None  # type: Optional[argparse.ArgumentParser]
        self._arg_help = {}  # type: Dict[str, Optional[str]]
        self._extra_sections = {} if extra_sections is None else extra_sections
        self._options_extra = {
            "prolog": options_prolog or "",
            "epilog": options_epilog or "",
        }

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def parser(self) -> argparse.ArgumentParser:
        assert self._parser is not None
        return self._parser

    @parser.setter
    def parser(self, parser: argparse.ArgumentParser):
        self._parser = parser

    @property
    def args(self) -> argparse.Namespace:
        """The parsed command line arguments"""
        assert self._args is not None
        return self._args

    @args.setter
    def args(self, args: argparse.Namespace):
        self._args = args

    @property
    def argument_help(self) -> Dict[str, Optional[str]]:
        return self._arg_help

    def get_synopsis(self, width: int = 80) -> str:
        optionals = []
        positionals = []
        for action in self.parser._actions:
            if action.option_strings:
                optionals.append(action)
            else:
                positionals.append(action)

        helpfmt = HelpFormatter(prog=self.parser.prog)
        format = helpfmt._format_actions_usage
        _, parts = format(
            optionals + positionals,
            self.parser._mutually_exclusive_groups,
            return_parts=True,
        )

        text = ""
        line = self.parser.prog
        lead = len(line) + 1
        for item in parts:
            if item is None:
                continue
            if len(line) + 1 + len(item) <= width:
                line += " " + item
            else:
                text += line + "\n"
                line = " " * lead + item
        text += line
        return text

    def get_options_text(self) -> str:
        prolog = self._options_extra["prolog"]
        if not isinstance(prolog, str):
            raise ValueError(
                f"Options prolog not of type str (received: {prolog})"
            )
        epilog = self._options_extra["epilog"]
        if not isinstance(epilog, str):
            raise ValueError(
                f"Options epilog not of type str (received: {epilog})"
            )

        text = [prolog]
        text.append("")
        for action in self.parser._get_optional_actions():
            desc = self._arg_help.get(action.dest)
            desc_source = "description"
            if desc is None:
                desc = action.help
                desc_source = "help"

            if desc is argparse.SUPPRESS or desc is None:
                continue

            if not isinstance(desc, str):
                raise ValueError(
                    f"Description for action {action.dest} found in "
                    f"{desc_source} attribute is not of type str "
                    f"(received type: {type(desc)})."
                )

            # TODO clean this up and make it testable
            if action.metavar is None:
                opts = ", ".join(action.option_strings)
            else:
                if action.option_strings[0].startswith(
                    2 * self.parser.prefix_chars
                ):
                    u = action.option_strings[0]
                    if action.choices and action.default:
                        v = f"[=({'|'.join(action.choices)})]"
                    elif action.choices:
                        v = f"=({'|'.join(action.choices)})"
                    else:
                        if action.nargs is None:
                            v = f"={action.metavar}"
                        elif action.nargs == "?":
                            v = f"[={action.metavar}]"
                        else:
                            v = f"={action.metavar}"
                    opts = f"{u}{v}"
                else:
                    opts = f"{action.option_strings[0]} {action.metavar}"
                    if len(action.option_strings) > 1:
                        opts += (
                            f", {action.option_strings[1]}={action.metavar}"
                        )

            text.append(opts)
            text.append(".RS 4")
            text.append(desc)
            text.append(".RE")
            text.append(".PP")

        for action in self.parser._get_positional_actions():
            desc = self._arg_help.get(action.dest)
            desc_source = "description"
            if desc is None:
                desc = action.help
                desc_source = "help"

            if desc is argparse.SUPPRESS or desc is None:
                continue

            if not isinstance(desc, str):
                raise ValueError(
                    f"Description for action {action.dest} found in "
                    f"{desc_source} attribute is not of type str "
                    f"(received type: {type(desc)})."
                )

            if action.nargs == "?":
                text.append(f"[{action.dest}]")
            else:
                text.append(f"<{action.dest}>")
            text.append(".RS 4")
            text.append(desc)
            text.append(".RE")
            text.append(".PP")

        text.append(epilog)
        return "\n".join(text)

    @abc.abstractmethod
    def create_manpage(self) -> ManPage:
        pass
