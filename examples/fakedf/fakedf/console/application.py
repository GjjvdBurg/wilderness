# -*- coding: utf-8 -*-

from fakedf.__version__ import __version__

from wilderness import Application

from ._docs import DOCS


class FakeDFApplication(Application):
    def __init__(self):
        super().__init__(
            "fakedf",
            version=__version__,
            title="report file system usage",
            author="John Doe",
            add_help=False,
            description=DOCS["description"],
            extra_sections=DOCS["extra"],
            prolog=DOCS["options"]["prolog"],
            epilog=DOCS["options"]["epilog"] + "\n\n" + DOCS["footer"],
            options_prolog=DOCS["options"]["prolog"],
            options_epilog=DOCS["options"]["epilog"],
        )

    def register(self):
        self.add_argument(
            "--help", action="help", help="show this help message and exit"
        )
        self.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="include pseudo, duplicate, inaccessible file systems",
        )
        self.add_argument(
            "-B",
            "--block-size",
            metavar="SIZE",
            help=(
                "scale sizes by SIZE before printing them; e.g., '-BM' "
                "prints sizes in units of 1,048,576 bytes; see SIZE "
                "format below"
            ),
        )
        self.add_argument(
            "-h",
            "--human-readable",
            action="store_true",
            help="print sizes in powers of 1024 (e.g., 1023M)",
        )
        self.add_argument(
            "-H",
            "--si",
            action="store_true",
            help="print sizes in powers of 1000 (e.g., 1.1G)",
        )
        self.add_argument(
            "-i",
            "--inodes",
            action="store_true",
            help="list inode information instead of block usage",
        )
        self.add_argument(
            "-k",
            action="store_true",
            help="like --block-size=1K",
        )
        self.add_argument(
            "-l",
            "--local",
            action="store_true",
            help="limit listing to local file systems",
        )
        self.add_argument(
            "--no-sync",
            action="store_true",
            help="do not invoke sync before getting usage info (default)",
        )
        self.add_argument(
            "--output",
            metavar="FIELD_LIST",
            nargs="?",
            help=(
                "use the output format defined by FIELD_LIST, or print "
                "all fields if FIELD_LIST is omitted."
            ),
        )
        self.add_argument(
            "-P",
            "--portability",
            action="store_true",
            help="use the POSIX output format",
        )
        self.add_argument(
            "--sync",
            action="store_true",
            help="invoke sync before getting usage info",
        )
        self.add_argument(
            "--total",
            action="store_true",
            help=(
                "elide all entries insignificant to available space, "
                "and produce a grand total"
            ),
        )
        self.add_argument(
            "-t",
            "--type",
            metavar="TYPE",
            help="limit listing to the file system of type TYPE",
        )
        self.add_argument(
            "-T",
            "--print-type",
            action="store_true",
            help="print file system type",
        )
        self.add_argument(
            "-x",
            "--exclude-type",
            metavar="TYPE",
            help="limit listing to file systems not of type TYPE",
        )
        self.add_argument("-v", action="store_true", help="(ignored)")
        self.add_argument("--version", action="version", version=__version__)

    def handle(self) -> int:
        print(f"Running fakedf with options: {self.args}")
        return 0


def build_application() -> Application:
    app = FakeDFApplication()
    return app
