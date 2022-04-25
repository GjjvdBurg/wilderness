# -*- coding: utf-8 -*-

"""Unit tests for help formatter

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.
"""

import sys
import unittest

from wilderness._argparse import ArgumentParser
from wilderness.formatter import HelpFormatter


class HelpFormatterTestCase(unittest.TestCase):

    maxDiff = None

    def test__fill_text_1(self):
        text = "Hello\nWorld"
        formatter = HelpFormatter("test")
        out = formatter._fill_text(text, 80, "")
        exp = "Hello\nWorld"
        self.assertEqual(out, exp)

    def test__fill_text_2(self):
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        formatter = HelpFormatter("test")
        out = formatter._fill_text(text, 65, "")
        explines = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut",
            "enim ad minim veniam, quis nostrud exercitation ullamco laboris",
            "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in",
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat",
            "nulla pariatur. Excepteur sint occaecat cupidatat non proident,",
            "sunt in culpa qui officia deserunt mollit anim id est laborum.",
        ]
        exp = "\n".join(explines)
        self.assertEqual(out, exp)

    def test__fill_text_3(self):
        text = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut "
            "enim ad minim veniam, quis nostrud exercitation ullamco laboris "
            "nisi ut aliquip ex ea commodo consequat.\n\nDuis aute irure "
            "dolor in reprehenderit in voluptate velit esse cillum dolore eu "
            "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non "
            "proident, sunt in culpa qui officia deserunt mollit anim id est "
            "laborum."
        )
        formatter = HelpFormatter("test")
        out = formatter._fill_text(text, 65, "")
        explines = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut",
            "enim ad minim veniam, quis nostrud exercitation ullamco laboris",
            "nisi ut aliquip ex ea commodo consequat.",
            "",
            "Duis aute irure dolor in reprehenderit in voluptate velit esse",
            "cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat",
            "cupidatat non proident, sunt in culpa qui officia deserunt mollit",
            "anim id est laborum.",
        ]
        exp = "\n".join(explines)
        self.assertEqual(out, exp)

    def test__format_actions_usage_1(self):
        parser = ArgumentParser(prog="test", formatter_class=HelpFormatter)
        grp = parser.add_mutually_exclusive_group()
        grp.add_argument(
            "-p", "--plain", action="store_true", help="plain help"
        )
        grp.add_argument("-j", "--json", action="store_true", help="json help")
        thehelp = parser.format_help()

        minor = sys.version_info.minor
        optstr = "options" if minor >= 10 else "optional arguments"
        exp = (
            f"usage: test [-p | --plain | -j | --json]\n\n{optstr}:\n"
            "  -h, --help   show this help message and exit\n"
            "  -p, --plain  plain help\n"
            "  -j, --json   json help\n"
        )
        self.assertEqual(thehelp, exp)


if __name__ == "__main__":
    unittest.main()
