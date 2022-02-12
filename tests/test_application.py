# -*- coding: utf-8 -*-

import unittest

from wilderness import Application
from wilderness.help import HelpCommand
from wilderness.tester import Tester


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
        tester = Tester(app)
        tester.test_application()
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), helptext)

        # Test that we get help with only -h flag
        tester = Tester(app)
        tester.test_application(["-h"])
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), helptext)

        # Test that we get help with only --help
        tester = Tester(app)
        tester.test_application(["--help"])
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), helptext)

        # Test that we get help with --help and other arguments
        tester = Tester(app)
        tester.test_application(["-q", "--help"])
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), helptext)

        # Test that we get help when help command supplied
        tester = Tester(app)
        tester.test_application(["help"])
        self.assertEqual(tester.get_return_code(), 1)
        self.assertEqual(tester.get_stdout(), helptext)


if __name__ == "__main__":
    unittest.main()
