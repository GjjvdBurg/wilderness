# -*- coding: utf-8 -*-

import contextlib
import io
import unittest

from wilderness import Application
from wilderness.help import HelpCommand


class ApplicationTestCase(unittest.TestCase):
    def test_application_1(self):
        class TestApp(Application):
            def __init__(self):
                super().__init__(
                    "testapp",
                    version="0.1.0",
                    title="testapp title",
                    author="John Doe",
                    description="long description",
                    extra_sections={"test": "test section"},
                )

            def register(self):
                self.add_argument(
                    "-q",
                    "--quiet",
                    help="be quiet",
                    action="store_true",
                    description="Run in quiet mode",
                )

        app = TestApp()

        self.assertEqual(app.name, "testapp")
        self.assertEqual(app.author, "John Doe")
        self.assertEqual(app.version, "0.1.0")
        self.assertEqual(app.description, "long description")
        self.assertEqual(len(app.commands), 1)
        self.assertTrue(isinstance(app.commands[0], HelpCommand))

        helptext = "usage: testapp [-h] [-q] command ...\n"
        self.assertEqual(app.format_help(), helptext)

        # Test that we get help without any arguments
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            status = app.run()
        self.assertEqual(status, 1)
        self.assertEqual(buf.getvalue(), helptext)

        # Test that we get help with only -h flag
        test_args = ["-h"]
        buf = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(buf):
                status = app.run(args=test_args)
        self.assertEqual(status, 1)
        self.assertEqual(buf.getvalue(), helptext)

        # Test that we get help with only --help
        test_args = ["--help"]
        buf = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(buf):
                status = app.run(args=test_args)
        self.assertEqual(status, 1)
        self.assertEqual(buf.getvalue(), helptext)

        # Test that we get help with --help and other arguments
        test_args = ["-q", "--help"]
        buf = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(buf):
                status = app.run(args=test_args)
        self.assertEqual(status, 1)
        self.assertEqual(buf.getvalue(), helptext)

        # Test that we get help when help command supplied
        test_args = ["help"]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            status = app.run(args=test_args)
        self.assertEqual(status, 1)
        self.assertEqual(buf.getvalue(), helptext)


if __name__ == "__main__":
    unittest.main()
