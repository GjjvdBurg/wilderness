# -*- coding: utf-8 -*-

"""Tester class

This module contains the CommandTester class.

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.
"""

import contextlib
import io

from typing import List
from typing import Optional

from .application import Application


class Tester:
    def __init__(self, app: Application) -> None:
        self._app = app

    @property
    def application(self) -> Application:
        return self._app

    def clear(self):
        self._retcode = None
        self._io_stderr = None
        self._io_stdout = None

    def get_return_code(self) -> Optional[int]:
        return self._retcode

    def get_stdout(self) -> Optional[str]:
        if self._io_stdout is None:
            return None
        return self._io_stdout.getvalue()

    def get_stderr(self) -> Optional[str]:
        if self._io_stderr is None:
            return None
        return self._io_stderr.getvalue()

    def test_command(self, cmd_name: str, args: List[str]) -> None:
        self.clear()
        command = self.application.get_command(cmd_name)
        if command is None:
            raise ValueError(f"No such command: {cmd_name}")

        args.insert(0, cmd_name)
        parser = self.application._parser
        parser.exit_on_error = False
        parsed_args = parser.parse_args(args=args)
        command.set_args(parsed_args)

        self._io_stdout = io.StringIO()
        self._io_stderr = io.StringIO()

        with contextlib.redirect_stdout(self._io_stdout):
            with contextlib.redirect_stderr(self._io_stderr):
                self._retcode = command.handle()

    def test_application(self, args: Optional[List[str]] = None) -> None:
        self.clear()
        args = [] if args is None else args

        parser = self.application._parser
        parser.exit_on_error = False
        parsed_args = parser.parse_args(args=args)
        self.application.set_args(parsed_args)

        self._io_stdout = io.StringIO()
        self._io_stderr = io.StringIO()

        with contextlib.redirect_stdout(self._io_stdout):
            with contextlib.redirect_stderr(self._io_stderr):
                self._retcode = self.application.run()
