#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Do-nothing script for making a release

This idea comes from here: 
https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/

Author: Gertjan van den Burg
Date: 2019-07-23

"""

import abc
import os
import sys
import tempfile
import webbrowser

import colorama

URLS = {
    "CI": "https://github.com/GjjvdBurg/wilderness/actions",
    "tags": "https://github.com/GjjvdBurg/wilderness/tags",
}


def color_text(msg, color=None, style=None):
    colors = {
        "red": colorama.Fore.RED,
        "green": colorama.Fore.GREEN,
        "cyan": colorama.Fore.CYAN,
        "yellow": colorama.Fore.YELLOW,
        "magenta": colorama.Fore.MAGENTA,
        None: "",
    }
    styles = {
        "bright": colorama.Style.BRIGHT,
        "dim": colorama.Style.DIM,
        None: "",
    }
    pre = colors[color] + styles[style]
    post = colorama.Style.RESET_ALL
    return f"{pre}{msg}{post}"


def color_print(msg, color=None, style=None):
    print(color_text(msg, color=color, style=style))


def wait_for_enter():
    input(color_text("\nPress Enter to continue", style="dim"))
    print()


def get_package_name():
    with open("./setup.py", "r") as fp:
        nameline = next(
            (l.strip() for l in fp if l.startswith("NAME = ")), None
        )
        return nameline.split("=")[-1].strip().strip('"')


def get_package_version(pkgname):
    ctx = {}
    with open(f"{pkgname}/__version__.py", "r") as fp:
        exec(fp.read(), ctx)
    return ctx["__version__"]


class Step(metaclass=abc.ABCMeta):
    def pre(self, context):
        pass

    def post(self, context):
        wait_for_enter()

    def run(self, context):
        try:
            self.pre(context)
            self.action(context)
            self.post(context)
        except KeyboardInterrupt:
            color_print("\nInterrupted.", color="red")
            raise SystemExit(1)

    def instruct(self, msg):
        color_print(msg, color="green")

    def print_command(self, msg):
        color_print("Run:", color="cyan", style="bright")
        color_print("\t" + msg, color="cyan", style="bright")

    def print_and_execute(self, cmd):
        color_print(f"Going to run: {cmd}", color="magenta", style="bright")
        wait_for_enter()
        os.system(cmd)

    @abc.abstractmethod
    def action(self, context):
        """Action to perform for the step"""


class GitToMaster(Step):
    def action(self, context):
        self.instruct("Make sure you're on master and changes are merged in")
        self.print_command("git checkout master")


class UpdateChangelog(Step):
    def action(self, context):
        self.instruct(f"Update change log for version {context['version']}")
        self.print_command("vi CHANGELOG.md")


class UpdateReadme(Step):
    def action(self, context):
        self.instruct("Update readme if necessary")
        self.print_command("vi README.md")


class RunTests(Step):
    def action(self, context):
        self.instruct("Run the unit tests")
        self.print_and_execute("make test && make mypy")


class BumpVersionPackage(Step):
    def action(self, context):
        self.instruct("Update __version__.py with new version")
        self.print_and_execute(f"vi {context['pkgname']}/__version__.py")

    def post(self, context):
        wait_for_enter()
        context["version"] = self._get_version(context)

    def _get_version(self, context):
        # Get the version from the version file
        return get_package_version(context["pkgname"])


class MakeClean(Step):
    def action(self, context):
        self.print_and_execute("make clean")


class MakeDocs(Step):
    def action(self, context):
        self.print_and_execute("make docs")


class MakeDist(Step):
    def action(self, context):
        self.print_and_execute("make dist")


class PushToTestPyPI(Step):
    def action(self, context):
        self.print_and_execute(
            "twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
        )


class InstallFromTestPyPI(Step):
    def action(self, context):
        tmpvenv = tempfile.mkdtemp(prefix="wild_venv_")
        self.print_and_execute(
            f"python -m venv {tmpvenv} && source {tmpvenv}/bin/activate && "
            "pip install --no-cache-dir --index-url "
            "https://test.pypi.org/simple/ "
            "--extra-index-url https://pypi.org/simple "
            f"{context['pkgname']}=={context['version']}"
        )
        context["tmpvenv"] = tmpvenv


class TestPackage(Step):
    def action(self, context):
        self.instruct(
            f"Ensure that the following command gives version {context['version']}"
        )
        self.print_and_execute(
            f"source {context['tmpvenv']}/bin/activate && pip list | grep {context['pkgname']}"
        )


class RemoveVenv(Step):
    def action(self, context):
        self.print_and_execute(f"rm -rf {context['tmpvenv']}")


class GitTagVersion(Step):
    def action(self, context):
        self.print_and_execute(
            f"git tag -s "
            f"-m \"Wilderness Release v{context['version']}\" "
            f"v{context['version']}"
        )


class GitAdd(Step):
    def action(self, context):
        self.instruct("Add everything to git and commit")
        self.print_command("git gui")


class GitAddRelease(Step):
    def action(self, context):
        self.instruct("Add Changelog & Readme to git")
        self.instruct(
            f"Commit with title: {context['pkgname']} Release {context['version']}"
        )
        self.instruct("Embed changelog in body commit message")
        self.print_and_execute("git gui")


class PushToPyPI(Step):
    def action(self, context):
        self.print_and_execute("twine upload dist/*")


class PushToGitHub(Step):
    def action(self, context):
        self.print_and_execute("git push -u --tags origin master")


class WaitForCI(Step):
    def action(self, context):
        webbrowser.open(URLS["CI"])
        self.instruct("Wait for CI to complete and verify that its successful")


class GitHubRelease(Step):
    def action(self, context):
        webbrowser.open(URLS["tags"])
        self.instruct("Create release from tag and embed release notes")


def main(target=None):
    colorama.init()
    procedure = [
        ("gittomaster", GitToMaster()),
        ("gitadd1", GitAdd()),
        ("clean1", MakeClean()),
        ("runtests", RunTests()),
        # trigger CI to run tests on all platforms
        ("push1", PushToGitHub()),
        ("ci1", WaitForCI()),
        ("bumpversion", BumpVersionPackage()),
        ("changelog", UpdateChangelog()),
        ("readme", UpdateReadme()),
        ("dist", MakeDist()),
        ("testpypi", PushToTestPyPI()),
        ("install", InstallFromTestPyPI()),
        ("testpkg", TestPackage()),
        ("remove_venv", RemoveVenv()),
        ("addrelease", GitAddRelease()),
        ("pypi", PushToPyPI()),
        ("tagfinal", GitTagVersion()),
        ("push2", PushToGitHub()),
        ("gh_release", GitHubRelease()),
    ]
    context = {}
    context["pkgname"] = get_package_name()
    context["version"] = get_package_version(context["pkgname"])
    skip = True if target else False
    for name, step in procedure:
        if not name == target and skip:
            continue
        skip = False
        step.run(context)
    color_print("\nDone!", color="yellow", style="bright")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    main(target=target)
