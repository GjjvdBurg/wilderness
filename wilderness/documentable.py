# -*- coding: utf-8 -*-

import argparse

from typing import Optional

from .formatter import HelpFormatter
from .manpages import ManPage


class DocumentableMixin:
    _description = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    def get_synopsis(self, width: int = 80) -> str:
        optionals = []
        positionals = []
        for action in self._parser._actions:
            if action.option_strings:
                optionals.append(action)
            else:
                positionals.append(action)

        helpfmt = HelpFormatter(prog=self._parser.prog)
        format = helpfmt._format_actions_usage
        _, parts = format(
            optionals + positionals,
            self._parser._mutually_exclusive_groups,
            return_parts=True,
        )

        text = ""
        line = self._parser.prog
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
        text = []
        for action in self._parser._get_optional_actions():
            desc = self._arg_help.get(action.dest, action.help)
            if desc is argparse.SUPPRESS or desc is None:
                continue

            # TODO clean this up
            if action.metavar is None:
                opts = ", ".join(action.option_strings)
            else:
                if action.option_strings[0].startswith(
                    2 * self._parser.prefix_chars
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
        for action in self._parser._get_positional_actions():
            desc = self._arg_help.get(action.dest, action.help)
            if desc is argparse.SUPPRESS or desc is None:
                continue
            text.append(f"<{action.dest}>")
            text.append(".RS 4")
            text.append(desc)
            text.append(".RE")
            text.append(".PP")
        return "\n".join(text)

    def populate_manpage(self, man: ManPage) -> None:
        man.add_section_synopsis(self.get_synopsis())
        man.add_section("description", self.description)
        man.add_section("options", self.get_options_text())
        for sec in self._extra_sections:
            man.add_section(sec, self._extra_sections[sec])
