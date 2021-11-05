# -*- coding: utf-8 -*-

"""Code to generate manpages

"""

import datetime as dt
import os
import re

from distutils.core import Command

from typing import TYPE_CHECKING
from typing import List
from typing import Optional

if TYPE_CHECKING:
    from wilderness.application import Application


class ManPage:
    def __init__(
        self,
        application_name: str,
        author: Optional[str] = "",
        command_name: Optional[str] = None,
        date: Optional[str] = None,
        title: Optional[str] = None,
        version: Optional[str] = None,
    ):

        self._application_name = application_name
        self._command_name = command_name
        self._version = version
        date = dt.date.today().strftime("%Y-%m-%d") if date is None else date

        self._title = title
        self._metadata = {
            "Title": self.name,
            "Author": author,
            "Generator": "Wilderness <https://pypi.org/project/wilderness>",
            "Date": date,
            "Manual": f"{self._application_name} Manual",
            "Source": f"{self._application_name} {self._version}",
            "Language": "English",
        }

        # Must be last
        self._page = []
        self._page.extend(self.metadata())
        self._page.append(self.header())
        self._page.extend(self.preamble())
        self._page.append(self.section_name())

    @property
    def name(self) -> str:
        app = self._application_name
        cmd = self._command_name
        if cmd is None:
            return app
        return f"{app}-{cmd}"

    def metadata(self) -> List[str]:
        text = ["'\\\" t"]  # This invokes the gtbl preprocessor (unused)

        # Metadata
        maxlen = max(map(len, self._metadata.keys()))
        for key, value in self._metadata.items():
            text.append(f'.\\"{key.rjust(maxlen + 1)}: {value}')
        text.append('.\\"')
        return text

    def preamble(self) -> List[str]:
        text = []

        # Portability stuff
        text.append('.\\" ' + "-" * 65)
        text.append('.\\" * Define some portability stuff')
        text.append('.\\" ' + "-" * 65)
        text.append('.\\" ' + "~" * 65)
        text.append('.\\" http://bugs.debian.org/507673')
        text.append(
            '.\\" http://lists.gnu.org/archive/html/groff/2009-02/msg00013.html'
        )
        text.append('.\\" ' + "~" * 65)
        text.append(".ie \\n(.g .ds Aq \\(aq")
        text.append(".el       .ds Aq '")

        # Default formatting
        text.append('.\\" ' + "-" * 65)
        text.append('.\\" * set default formatting *')
        text.append('.\\" ' + "-" * 65)
        text.append('.\\" disable hyphenation')
        text.append(".nh")
        text.append('.\\" disable justification')
        text.append(".ad l")

        # Banner
        text.append('.\\" ' + "-" * 65)
        text.append('.\\" * MAIN CONTENT STARTS HERE *')
        text.append('.\\" ' + "-" * 65)
        return text

    def header(self) -> str:
        app = self._application_name
        date = self._metadata["Date"].replace("-", "\\-")
        version = self._version.replace(".", "\\&.")
        header = (
            f'.TH "{self.name.upper()}" "1" "{date}" '
            f'"{app.capitalize()} {version}" '
            f'"{app.capitalize()} Manual"'
        )
        return header

    def section_name(self) -> str:
        return f'.SH "NAME"\n{self.name} \\- {self._title}'

    def add_section_synopsis(self, synopsis: str) -> None:
        text = [
            '.SH "SYNOPSIS"',
            ".sp",
            ".nf",
            f"\\fI{self.groffify(synopsis)}",
            ".fi",
            ".sp",
        ]
        self._page.extend(text)

    def add_section(self, label: str, text: str) -> None:
        text = [
            f'.SH "{label.upper()}"',
            ".sp",
            self.groffify(text),
        ]
        self._page.extend(text)

    def groffify(self, text: str) -> str:
        output = []

        lines = text.split("\n")
        for line in lines:
            if line.startswith("* "):
                output.append(".RS 4")
                output.append(".ie n \\{\\")
                output.append("\\h'-04'\\(bu\\h'+03'\\c")
                output.append(".\\}")
                output.append(".el \\{\\")
                output.append(".sp -1")
                output.append(".IP \\(bu 2.3")
                output.append(".\\}")
                output.append(self.groffiy_line(line[2:]))
                output.append(".RE")
            elif line.startswith("\t"):
                output.append(".RS 4")
                output.append(self.groffiy_line(line[1:]))
                output.append(".RE")
            elif m := re.match("^\ ?\d+\.\ ", line):
                label, rest = line[m.start() : m.end()], line[m.end() :]
                output.append(f"\\fB{label}\\fR{self.groffiy_line(rest)}")
                output.append(".br")
            elif line in ["", "\n"]:
                output.append(".sp")
            else:
                output.append(self.groffiy_line(line))
        return "\n".join(output)

    def groffiy_line(self, line: str) -> str:
        line = line.replace("\\", "\\e")
        line = line.replace("-", "\\-")
        line = line.replace("...", "\\&...")
        line = line.replace("\n\n", "\n.sp\n")
        return line

    def export(self, output_dir: str) -> str:
        filename = os.path.join(output_dir, f"{self.name}.1")
        with open(filename, "w") as fp:
            fp.write("\n".join(self._page))
        return filename


def manpage_builder(
    app: "Application", output_directory: str = "man"
) -> Command:
    class build_manpages(Command):
        description = f"Generate manpages for {app.name}"
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            os.makedirs(output_directory, exist_ok=True)
            man = app.create_manpage()
            filename = man.export(output_directory)
            print(f"Wrote application manpage to {filename}")
            for cmd in app.commands:
                man = cmd.create_manpage()
                filename = man.export(output_directory)
                print(f"Wrote application manpage to {filename}")

    return build_manpages