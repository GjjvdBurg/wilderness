# -*- coding: utf-8 -*-

"""HelpFormatter

We have a slightly adjusted HelpFormatter that we use for the manpages.

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.
"""

import argparse
import re
import textwrap

from typing import Dict


class HelpFormatter(argparse.HelpFormatter):
    def _fill_text(self, text, width, indent):
        # Minor change to _fill_text to keep newlines provided by the user in
        # the prolog and epilog.
        lines = text.splitlines()
        new_lines = []
        for line in lines:
            new_line = textwrap.fill(
                line,
                width,
                initial_indent=indent,
                subsequent_indent=indent,
            )
            new_lines.append(new_line)
        new_text = "\n".join(new_lines)
        return new_text

    def _format_actions_usage(self, actions, groups, return_parts=False):
        # find group indices and identify actions in groups
        group_actions = set()
        inserts = {}  # type: Dict[int, str]
        for group in groups:
            try:
                start = actions.index(group._group_actions[0])
            except ValueError:
                continue
            else:
                end = start + len(group._group_actions)
                if actions[start:end] == group._group_actions:
                    for action in group._group_actions:
                        group_actions.add(action)
                    if not group.required:
                        if start in inserts:
                            inserts[start] += " ["
                        else:
                            inserts[start] = "["
                        if end in inserts:
                            inserts[end] += "]"
                        else:
                            inserts[end] = "]"
                    else:
                        if start in inserts:
                            inserts[start] += " ("
                        else:
                            inserts[start] = "("
                        if end in inserts:
                            inserts[end] += ")"
                        else:
                            inserts[end] = ")"
                    for i in range(start + 1, end):
                        inserts[i] = "|"

        # collect all actions format strings
        parts = []
        for i, action in enumerate(actions):
            if isinstance(action, argparse._HelpAction):
                continue

            # produce all arg strings
            if not action.option_strings:
                default = self._get_default_metavar_for_positional(action)
                part = self._format_args(action, default)

                # if it's in a group, strip the outer []
                if action in group_actions:
                    if part[0] == "[" and part[-1] == "]":
                        part = part[1:-1]
                else:
                    if action.nargs == "?":
                        pass
                    else:
                        part = "<%s>" % part

                # add the action string to the list
                parts.append(part)

            # produce the first way to invoke the option in brackets
            else:
                part = self._format_part(action, group_actions)

                # add the action string to the list
                parts.append(part)

        # insert things at the necessary indices
        for i in sorted(inserts, reverse=True):
            parts[i:i] = [inserts[i]]

        # join all the action items with spaces
        text = " ".join([item for item in parts if item is not None])

        # clean up separators for mutually exclusive groups
        open = r"[\[(]"
        close = r"[\])]"
        text = re.sub(r"(%s) " % open, r"\1", text)
        text = re.sub(r" (%s)" % close, r"\1", text)
        text = re.sub(r"%s *%s" % (open, close), r"", text)
        text = re.sub(r"\(([^|]*)\)", r"\1", text)
        text = text.strip()

        if return_parts:
            return text, parts

        # return the text
        return text

    def _format_part(self, action, group_actions):
        option_string = action.option_strings[0]

        # if the Optional doesn't take a value, format is:
        #    -s or --long
        if action.nargs == 0:
            if len(action.option_strings) == 2:
                part = " | ".join(action.option_strings)
            else:
                part = action.option_strings[0]

        # TODO: get prefix chars from parser
        elif option_string.startswith("--"):
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            if args_string.startswith("["):
                part = "%s[=%s" % (option_string, args_string[1:])
            else:
                part = "%s=%s" % (option_string, args_string)

        elif len(action.option_strings) == 2:
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            part0 = "%s %s" % (action.option_strings[0], args_string)
            part1 = "%s=%s" % (action.option_strings[1], args_string)
            part = "%s | %s" % (part0, part1)

        # if the Optional takes a value, format is:
        #    -s ARGS or --long ARGS
        else:
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            part = "%s %s" % (option_string, args_string)

        # make it look optional if it's not required or in a group
        if not action.required and action not in group_actions:
            part = "[%s]" % part
        else:
            raise NotImplementedError
        return part
