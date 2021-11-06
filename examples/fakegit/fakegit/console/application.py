# -*- coding: utf-8 -*-

from fakegit.__version__ import __version__

from wilderness import Application

from .commands import CloneCommand
from .commands import CommitCommand
from .commands import FetchCommand
from .commands import InitCommand


class FakeGitApplication(Application):

    _description = (
        "FakeGit is a fast, scalable, distributed revision control system "
        "with an unusually rich command set that provides both high-level "
        "operations and full access to internals."
        "\n\n"
        "See gittutorial(7) to get started, then see giteveryday(7) for a "
        "useful minimum set of commands. The FakeGit User’s Manual[1] has a "
        "more in-depth introduction."
        "\n\n"
        "After you mastered the basic concepts, you can come back to this "
        "page to learn what commands FakeGit offers. You can learn more about "
        'individual FakeGit commands with "git help command". gitcli(7) '
        "manual page gives you an overview of the command-line command syntax."
        "\n\n"
        "A formatted and hyperlinked copy of the latest FakeGit "
        "documentation can be viewed at "
        "https://git.github.io/htmldocs/git.html or https://git-scm.com/docs."
    )
    _extra = {
        "git commands": (
            'We divide Git into high level ("porcelain") commands and low '
            'level ("plumbing") commands.'
        ),
        "Configuration Mechanism": (
            "Git uses a simple text format to store customizations that are "
            "per repository and are per user. Such a configuration file may "
            "look like this:"
            "\n\n"
            "\t#\n"
            "\t# A '#' or ';' character indicates a comment.\n"
            "\t#\n"
            "\n"
            "\t; core variables\n"
            "\t[core]\n"
            "\t\t; Don't trust file modes\n"
            "\t\tfilemode = false\n"
            "\n"
            "\t; user identity\n"
            "\t[user]\n"
            '\t\tname = "Junio C Hamano"\n'
            '\t\temail = "gitster@pobox.com"\n'
            "\n"
            "Various commands read from the configuration file and adjust "
            "their operation accordingly. See git-config(1) for a list and "
            "more details about the configuration mechanism."
        ),
        "notes": (
            " 1. Git User’s Manual\n"
            "    file:///usr/share/doc/git-doc/user-manual.html"
            "\n\n"
            " 2. Trace2 documentation\n"
            "    file:///usr/share/doc/git-doc/technical/api-trace2.html"
            "\n\n"
            " 3. Git concepts chapter of the user-manual\n"
            "    file:///usr/share/doc/git-doc/user-manual.html#git-concepts"
            "\n\n"
            " 4. howto\n"
            "    file:///usr/share/doc/git-doc/howto-index.html"
            "\n\n"
            " 5. Git API documentation\n"
            "    file:///usr/share/doc/git-doc/technical/api-index.html"
            "\n\n"
            " 6. git@vger.kernel.org\n"
            "    mailto:git@vger.kernel.org"
            "\n\n"
            " 7. git-security@googlegroups.com\n"
            "    mailto:git-security@googlegroups.com"
        ),
    }

    def __init__(self):
        super().__init__(
            "fakegit",
            version=__version__,
            title="the stupid content tracker",
            author="Jane Doe",
            description=self._description,
            extra_sections=self._extra,
        )

    def register(self):
        self.add_argument(
            "--version",
            help="show version information and exit",
            action="version",
            version=__version__,
            description=(
                "Prints the FakeGit suite version that the git program came from.\n\n"
                "This option is internally converted to git version ... and "
                "accepts the same options as the git-version(1) command. If "
                "--help is also given, it takes precedence over --version."
            ),
        )
        self.add_argument(
            "-C",
            metavar="<path>",
            help="change working directory",
            description=(
                "Run as if git was started in <path> instead of the current "
                "working directory. When multiple -C options are given, each "
                "subsequent non-absolute -C <path> is interpreted relative to "
                "the preceding -C <path>. If <path> is present but empty, e.g. "
                '-C "", then the current working directory is left '
                "unchanged."
                "\n\n"
                "This option affects options that expect path name like "
                "--git-dir and --work-tree in that their interpretations of "
                "the path names would be made relative to the working "
                "directory caused by the -C option. For example the "
                "following invocations are equivalent:"
                "\n\n"
                "\tgit --git-dir=a.git --work-tree=b -C c status"
                "\tgit --git-dir=c/a.git --work-tree=c/b status"
            ),
        )
        self.add_argument(
            "-c",
            metavar="<name>=<value>",
            help="pass a configuration parameter to the command",
            description=(
                "Pass a configuration parameter to the command. The value "
                "given will override values from configuration files. The "
                "<name> is expected in the same format as listed by git "
                "config (subkeys separated by dots)."
                "\n\n"
                "Note that omitting the = in git -c foo.bar ...  is allowed "
                "and sets foo.bar to the boolean true value (just like "
                "[foo]bar would in a config file). Including the equals "
                "but with an empty value (like git -c foo.bar= ...) sets "
                "foo.bar to the empty string which git config --type=bool "
                "will convert to false."
            ),
        )


def build_application() -> Application:
    app = FakeGitApplication()
    app.set_prolog("These are common Git commands used in various situations:")

    group = app.add_group("start a working area")
    group.add(CloneCommand())
    group.add(InitCommand())

    # group = app.add_group("work on the current change")
    # group.add(AddCommand())
    # group.add(MoveCommand())
    # group.add(RestoreCommand())
    # group.add(RemoveCommand())

    # group = app.add_group("examine the history and state")
    # group.add(BisectCommand())
    # group.add(DiffCommand())
    # group.add(GrepCommand())
    # group.add(LogCommand())

    group = app.add_group("grow, mark and tweak your common history")
    # group.add(BranchCommand())
    group.add(CommitCommand())
    # group.add(MergeCommand())

    group = app.add_group("collaborate (see also: git help workflows)")
    group.add(FetchCommand())
    # group.add(PullCommand())

    app.set_epilog(
        "'git help -a' and 'git help -g' list available subcommands and some\n"
        "concept guides. See 'git help <command>' or 'git help <concept>'\n"
        "to read about a specific subcommand or concept.\n"
        "See 'git help git' for an overview of the system."
    )
    return app
