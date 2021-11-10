# -*- coding: utf-8 -*-

import unittest

from wilderness import Application
from wilderness import Command


class GroupTestCase(unittest.TestCase):
    def test_group(self):
        class TestApp(Application):
            def __init__(self):
                super().__init__(
                    "testapp",
                    version="0.1.0",
                    title="testapp title",
                    author="John Doe",
                    description="long description",
                    extra_sections={"test": "test section"},
                    prolog="The prolog",
                    epilog="This is\n\nthe epilog",
                )

            def register(self):
                pass

        class CommandOne(Command):
            def __init__(self):
                super().__init__(
                    name="cmd1",
                    title="command 1 title",
                    description="command 1 description",
                )

            def handle(self):
                print("Running command one")

        class CommandTwo(Command):
            def __init__(self):
                super().__init__(
                    name="cmd2",
                    title="command 2 title",
                    description="command 2 description",
                )

            def handle(self):
                print("Running command two")

        app = TestApp()
        cmd1 = CommandOne()
        cmd2 = CommandTwo()

        group = app.add_group("group 1")
        group.add(cmd1)
        group.add(cmd2)

        self.assertEqual(group.application, app)
        self.assertEqual(group.title, "group 1")
        self.assertEqual(group.commands, [cmd1, cmd2])
        self.assertEqual(len(group), 2)

        actions = group.commands_as_actions()
        self.assertEqual(actions[0].dest, "cmd1")
        self.assertEqual(actions[0].help, "command 1 title")

        self.assertEqual(actions[1].dest, "cmd2")
        self.assertEqual(actions[1].help, "command 2 title")

        helptext = (
            "usage: testapp [-h] command ...\n"
            "\n"
            "The prolog\n"
            "\n"
            "group 1:\n"
            "  cmd1  command 1 title\n"
            "  cmd2  command 2 title\n"
            "\n"
            "This is\n\n"
            "the epilog\n"
        )
        self.assertEqual(app.format_help(), helptext)


if __name__ == "__main__":
    unittest.main()
