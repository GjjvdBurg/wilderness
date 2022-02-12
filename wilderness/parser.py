# -*- coding: utf-8 -*-

"""ArgumentParser override

Author: G.J.J. van den Burg
License: See the LICENSE file.
Copyright: 2021, G.J.J. van den Burg

This file is part of Wilderness.

"""

import argparse
import sys

from typing import Optional


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, exit_on_error=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.exit_on_error = exit_on_error

    def exit(self, status: Optional[int] = 0, message: Optional[str] = None):
        if message:
            self._print_message(message, sys.stderr)
        if self.exit_on_error:
            sys.exit(status)
