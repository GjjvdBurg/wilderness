# -*- coding: utf-8 -*-

import unittest

from wilderness import Application
from wilderness.help import HelpCommand
from wilderness.tester import Tester


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


class ApplicationTestCase(unittest.TestCase):
    def setUp(self):
        self._app = TestApp()
        self._helptext = "usage: testapp [-h] [-q] command ...\n"

    def test_application_base(self):
        app = self._app
        self.assertEqual(app.name, "testapp")
        self.assertEqual(app.author, "John Doe")
        self.assertEqual(app.version, "0.1.0")
        self.assertEqual(app.description, "long description")
        self.assertEqual(len(app.commands), 1)
        self.assertTrue(isinstance(app.commands[0], HelpCommand))

    def test_application_help_1(self):
        self.assertEqual(self._app.format_help(), self._helptext)

    def test_application_help_2(self):
        # Test that we get help without any arguments
        tester = Tester(self._app)
        tester.test_application()
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), self._helptext)

    def test_application_help_3(self):
        # Test that we get help with only -h flag
        tester = Tester(self._app)
        tester.test_application(["-h"])
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), self._helptext)

    def test_application_help_4(self):
        # Test that we get help with only --help
        tester = Tester(self._app)
        tester.test_application(["--help"])
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), self._helptext)

    def test_application_help_5(self):
        # Test that we get help with --help and other arguments
        tester = Tester(self._app)
        tester.test_application(["-q", "--help"])
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), self._helptext)

    def test_application_help_6(self):
        # Test that we get help when help command supplied
        tester = Tester(self._app)
        tester.test_application(["help"])
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), self._helptext)


if __name__ == "__main__":
    unittest.main()
