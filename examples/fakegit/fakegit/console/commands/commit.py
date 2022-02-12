# -*- coding: utf-8 -*-

from wilderness.command import Command


class CommitCommand(Command):
    _description = (
        "Create a new commit containing the current contents of the "
        "index and the given log message describing the changes. The "
        "new commit is a direct child of HEAD, usually the tip of the "
        "current branch, and the branch is updated to point to it "
        "(unless no branch is associated with the working tree, in "
        'which case HEAD is "detached" as described in '
        "git-checkout(1))."
    )

    def __init__(self):
        super().__init__(
            name="commit",
            title="Record changes to the repository",
            description=self._description,
        )

    def register(self):
        self.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="suppress summary after successful commit",
            description="Suppress commit summary message.",
        )
        self.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="show diff in commit message template",
            description=(
                "Show unified diff between the HEAD commit and what would be "
                "committed at the bottom of the commit message template to "
                "help the user describe the commit by reminding what changes "
                "the commit has. Note that this diff output doesn't have its "
                "lines prefixed with #. This diff will not be a part of the "
                "commit message. See the commit.verbose configuration "
                "variable in git-config(1).\n\nIf specified twice, show in "
                "addition the unified diff between what would be committed "
                "and the worktree files, i.e. the unstaged changes to the "
                "tracked files."
            ),
        )

        self.add_argument(
            "--amend",
            action="store_true",
            help="amend previous commit",
            description=(
                "Replace the tip of the current branch by creating a new "
                "commit. The recorded tree is prepared as usual (including "
                "the effect of the -i and -o options and explicit pathspec), "
                "and the message from the original commit is used as the "
                "starting point, instead of an empty message, when no other "
                "message is specified from the command line via options such "
                "as -m, -F, -c, etc. The new commit has the same parents and "
                "author as the current one (the --reset-author option can "
                "countermand this)."
            ),
        )

    def handle(self):
        print("Running git commit, amend=%s" % self.args.amend)
