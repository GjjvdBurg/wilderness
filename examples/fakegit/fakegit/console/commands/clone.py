# -*- coding: utf-8 -*-

from wilderness.command import Command


class CloneCommand(Command):

    _description = (
        "Clones a repository into a newly created directory, creates "
        "remote-tracking branches for each branch in the cloned repository "
        "(visible using git branch --remotes), and creates and checks out an "
        "initial branch that is forked from the cloned repository’s currently "
        "active branch.\n\n"
        "After the clone, a plain git fetch without arguments will update all "
        "the remote-tracking branches, and a git pull without arguments will "
        "in addition merge the remote master branch into the current master "
        'branch, if any (this is untrue when "--single-branch" is given; '
        "see below).\n\n"
        "This default configuration is achieved by creating references to the "
        "remote branch heads under refs/remotes/origin and by initializing "
        "remote.origin.url and remote.origin.fetch configuration variables."
    )
    _git_urls = (
        "In general, URLs contain information about the transport protocol, "
        "the address of the remote server, and the path to the repository. "
        "Depending on the transport protocol, some of this information may be "
        "absent.\n\n"
        "Git supports ssh, git, http, and https protocols (in addition, ftp, "
        "and ftps can be used for fetching, but this is inefficient and "
        "deprecated; do not use it).\n\n"
        "The native transport (i.e. git:// URL) does no authentication and "
        "should be used with caution on unsecured networks.\n\n"
        "The following syntaxes may be used with them:\n"
        "\n"
        "* ssh://[user@]host.xz[:port]/path/to/repo.git/\n\n"
        "* git://host.xz[:port]/path/to/repo.git/\n\n"
        "* http[s]://host.xz[:port]/path/to/repo.git/\n\n"
        "* ftp[s]://host.xz[:port]/path/to/repo.git/\n\n"
        "\n"
        "An alternative scp-like syntax may also be used with the ssh "
        "protocol:\n"
        "\n"
        "* [user@]host.xz:path/to/repo.git/\n"
        "\n"
        "This syntax is only recognized if there are no slashes before the "
        "first colon. This helps differentiate a local path that contains a "
        "colon. For example the local path foo:bar could be specified as an "
        "absolute path or ./foo:bar to avoid being misinterpreted as an ssh "
        "url.\n"
        "\n"
        "The ssh and git protocols additionally support ~username expansion:"
        "\n\n"
        "* ssh://[user@]host.xz[:port]/~[user]/path/to/repo.git/\n\n"
        "* git://host.xz[:port]/~[user]/path/to/repo.git/\n\n"
        "* [user@]host.xz:/~[user]/path/to/repo.git/\n\n"
        "For local repositories, also supported by Git natively, the "
        "following syntaxes may be used:"
        "\n\n"
        "* /path/to/repo.git/\n\n"
        "* file:///path/to/repo.git/\n\n"
        "These two syntaxes are mostly equivalent, except the former implies "
        "--local option.\n"
        "\n"
        "git clone, git fetch and git pull, but not git push, will also "
        "accept a suitable bundle file. See git-bundle(1).\n\n"
        "When Git doesn’t know how to handle a certain transport protocol, "
        "it attempts to use the remote-<transport> remote helper, if one "
        "exists. To explicitly request a remote helper, the following syntax "
        "may be used:\n\n"
        "* <transport>::<address>\n\n"
        "where <address> may be a path, a server and path, or an arbitrary "
        "URL-like string recognized by the specific remote helper being "
        "invoked. See gitremote-helpers(7) for details."
        "\n\n"
        "If there are a large number of similarly-named remote repositories "
        "and you want to use a different format for them (such that the URLs "
        "you use will be rewritten into URLs that work), you can create a "
        "configuration section of the form:\n\n"
        '\t\t[url "<actual url base>"]\n'
        "\t\t\tinsteadOf = <other url base>\n"
        "\n"
        "For example, with this:\n"
        "\n"
        '\t\t[url "git://git.host.xz/"]\n'
        "\t\t\tinsteadOf = host.xz:/path/to/\n"
        "\t\t\tinsteadOf = work:\n"
        "\n"
        'a URL like "work:repo.git" or like "host.xz:/path/to/repo.git" '
        "will be rewritten in any context that takes a URL to be "
        '"git://git.host.xz/repo.git".\n\n'
        "If you want to rewrite URLs for push only, you can create a "
        "configuration section of the form:"
        "\n\n"
        '\t\t[url "<actual url base>"]\n'
        "\t\t\tpushInsteadOf = <other url base>"
        "\n\n"
        "For example, with this:"
        "\n\n"
        '\t\t[url "ssh://example.org/"]\n'
        "\t\t\tpushInsteadOf = git://example.org/"
        "\n\n"
        'a URL like "git://example.org/path/to/repo.git" will be rewritten '
        'to "ssh://example.org/path/to/repo.git" for pushes, but pulls '
        "will still use the original URL."
    )
    _examples = (
        "* Clone from upstream:\n\n"
        "\t$ git clone git://git.kernel.org/pub/scm/.../linux.git my-linux\n"
        "\t$ cd my-linux\n"
        "\t$ make\n"
        "\n"
        "* Make a local clone that borrows from the current directory, "
        "without checking things out:\n\n"
        "\t$ git clone -l -s -n . ../copy\n"
        "\t$ cd ../copy\n"
        "\t$ git show-branch\n\n"
        "* Clone from upstream while borrowing from an existing local "
        "directory:\n\n"
        "\t$ git clone --reference /git/linux.git \\\n"
        "\t\tgit://git.kernel.org/pub/scm/.../linux.git \\\n"
        "\t\tmy-linux\n"
        "\t$ cd my-linux"
        "\n\n"
        "* Create a bare repository to publish your changes to the public:"
        "\n\n"
        "\t$ git clone --bare -l /home/proj/.git /pub/scm/proj.git"
    )

    def __init__(self):
        super().__init__(
            name="clone",
            title="Clone a repository into a new directory",
            description=self._description,
            extra_sections={
                "Git URLs": self._git_urls,
                "Examples": self._examples,
            },
        )

    def register(self):
        self.add_argument(
            "-l",
            "--local",
            action="store_true",
            help="to clone from a local repository",
            description=(
                "When the repository to clone from is on a local machine, "
                'this flag bypasses the normal "Git aware" transport '
                "mechanism and clones the repository by making a copy of "
                "HEAD and everything under objects and refs directories. The "
                "files under .git/objects/ directory are hardlinked to save "
                "space when possible."
                "\n\n"
                "If the repository is specified as a local path (e.g., "
                "/path/to/repo), this is the default, and --local is "
                "essentially a no-op. If the repository is specified as a "
                "URL, then this flag is ignored (and we never use the local "
                "optimizations). Specifying --no-local will override the "
                "default when /path/to/repo is given, using the regular Git "
                "transport instead."
                "\n\n"
                "NOTE: this operation can race with concurrent modification "
                "to the source repository, similar to running cp -r src dst "
                "while modifying src."
            ),
        )
        self.add_argument(
            "--no-hardlinks",
            action="store_true",
            help="don't use local hardlinks, always copy",
            description=(
                "Force the cloning process from a repository on a local "
                "filesystem to copy the files under the .git/objects "
                "directory instead of using hardlinks. This may be desirable "
                "if you are trying to make a back-up of your repository."
            ),
        )
        self.add_argument(
            "-s",
            "--shared",
            action="store_true",
            help="setup as shared repository",
            description=(
                "When the repository to clone is on the local machine, "
                "instead of using hard links, automatically setup "
                ".git/objects/info/alternates to share the objects with "
                "the source repository. The resulting repository starts "
                "out without any object of its own."
                "\n\n"
                "NOTE: this is a possibly dangerous operation; do not use "
                "it unless you understand what it does. If you clone your "
                "repository using this option and then delete branches "
                "(or use any other Git command that makes any existing "
                "commit unreferenced) in the source repository, some "
                "objects may become unreferenced (or dangling). These "
                "objects may be removed by normal Git operations (such as "
                "git commit) which automatically call git maintenance "
                "run --auto. (See git-maintenance(1).) If these objects "
                "are removed and were referenced by the cloned repository, "
                "then the cloned repository will become corrupt."
                "\n\n"
                "Note that running git repack without the --local option "
                "in a repository cloned with --shared will copy objects "
                "from the source repository into a pack in the cloned "
                "repository, removing the disk space savings of clone "
                "--shared. It is safe, however, to run git gc, which "
                "uses the --local option by default."
                "\n\n"
                "If you want to break the dependency of a repository "
                "cloned with --shared on its source repository, you can "
                "simply run git repack -a to copy all objects from the "
                "source repository into a pack in the cloned repository."
            ),
        )
        self.add_argument(
            "--reference",
            metavar="<repository>",
            help="reference repository",
            description=(
                "If the reference repository is on the local machine, "
                "automatically setup .git/objects/info/alternates to "
                "obtain objects from the reference repository. "
                "Using an already existing repository as an alternate "
                "will require fewer objects to be copied from the "
                "repository being cloned, reducing network and local "
                "storage costs."
                "\n\n"
                "NOTE: see the NOTE for the --shared option, and also "
                "the --dissociate option."
            ),
        )
        self.add_argument(
            "--reference-if-able",
            metavar="<repository>",
            help="reference repository",
            description=(
                "Similar to --reference, but when using the "
                "--reference-if-able, a non existing directory is "
                "skipped with a warning instead of aborting the clone."
                "\n\n"
                "NOTE: see the NOTE for the --shared option, and also "
                "the --dissociate option."
            ),
        )
        self.add_argument(
            "--dissociate",
            action="store_true",
            help="use --reference only while cloning",
            description=(
                "Borrow the objects from reference repositories specified "
                "with the --reference options only to reduce network "
                "transfer, and stop borrowing from them after a clone is "
                "made by making necessary local copies of borrowed "
                "objects. This option can also be used when cloning "
                "locally from a repository that already borrows objects "
                "from another repository—the new repository will borrow "
                "objects from the same repository, and this option can be "
                "used to stop the borrowing."
            ),
        )
        self.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="be more quiet",
            description=(
                "Operate quietly. Progress is not reported to the "
                "standard error stream."
            ),
        )
        self.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="be more verbose",
            description=(
                "Run verbosely. Does not affect the reporting of progress "
                "status to the standard error stream"
            ),
        )
        self.add_argument(
            "--progress",
            action="store_true",
            help="force progress reporting",
            description=(
                "Progress status is reported on the standard error stream "
                "by default when it is attached to a terminal, unless "
                "--quiet is specified. This flag forces progress status even "
                "if the standard error stream is not directed to a terminal."
            ),
        )
        self.add_argument(
            "--server-option",
            help="option to transmit",
            metavar="<option>",
            description=(
                "Transmit the given string to the server when communicating "
                "using protocol version 2. The given string must not contain "
                "a NUL or LF character. The server’s handling of server "
                "options, including unknown ones, is server-specific. When "
                "multiple --server-option=<option> are given, they are all "
                "sent to the other side in the order listed on the command "
                "line."
            ),
        )
        self.add_argument(
            "-n",
            "--no-checkout",
            help="don't create a checkout",
            action="store_true",
            description=(
                "No checkout of HEAD is performed after the clone is complete."
            ),
        )
        self.add_argument(
            "--reject-shallow",
            help="don't clone shallow repository",
            action="store_true",
            description=(
                "Fail if the source repository is a shallow repository. The "
                "clone.rejectShallow configuration variable can be used to "
                "specify the default."
            ),
        )
        self.add_argument(
            "--bare",
            help="create a bare repository",
            action="store_true",
            description=(
                "Make a bare Git repository. That is, instead of creating "
                "<directory> and placing the administrative files in "
                "<directory>/.git, make the <directory> itself the "
                "$GIT_DIR. This obviously implies the --no-checkout because "
                "there is nowhere to check out the working tree. Also the "
                "branch heads at the remote are copied directly to "
                "corresponding local branch heads, without mapping them to "
                "refs/remotes/origin/. When this option is used, neither "
                "remote-tracking branches nor the related configuration "
                "variables are created."
            ),
        )
        self.add_argument(
            "--sparse",
            help=(
                "initialize sparse-checkout file to include only files at root"
            ),
            action="store_true",
            description=(
                "Initialize the sparse-checkout file so the working directory "
                "starts with only the files in the root of the repository. "
                "The sparse-checkout file can be modified to grow the working "
                "directory as needed."
            ),
        )

        ###

        self.add_argument(
            "--no-tags",
            action="store_true",
            help=(
                "don't clone any tags, and make later fetches not to "
                "follow them"
            ),
            description=(
                "Don’t clone any tags, and set "
                "remote.<remote>.tagOpt=--no-tags in the config, ensuring "
                "that future git pull and git fetch operations won’t follow "
                "any tags. Subsequent explicit tag fetches will still "
                "work, (see git-fetch(1))."
                "\n\n"
                "Can be used in conjunction with --single-branch to clone "
                "and maintain a branch with no references other than a "
                "single cloned branch. This is useful e.g. to maintain "
                "minimal clones of the default branch of some repository for "
                "search indexing."
            ),
        )

        self.add_argument(
            "--recurse-submodules",
            metavar="<pathspec>",
            help="initialize submodules in the clone",
            nargs="?",
            description=(
                "After the clone is created, initialize and clone submodules "
                "within based on the provided pathspec. If no pathspec is "
                "provided, all submodules are initialized and cloned. This "
                "option can be given multiple times for pathspecs consisting "
                "of multiple entries. The resulting clone has "
                'submodule.active set to the provided pathspec, or "." '
                "(meaning all submodules) if no pathspec is provided."
                "\n\n"
                "Submodules are initialized and cloned using their default "
                "settings. This is equivalent to running git submodule "
                "update --init --recursive <pathspec> immediately after the "
                "clone is finished. This option is ignored if the cloned "
                "repository does not have a worktree/checkout (i.e. if any "
                "of --no-checkout/-n, --bare, or --mirror is given)"
            ),
        )

        self.add_argument(
            "repository",
            help="Repository to clone",
            description=(
                "The (possibly remote) repository to clone from. See the GIT "
                "URLS section below for more information on specifying "
                "repositories."
            ),
        )

    def handle(self):
        print(f"Running clone command with repository: {self.args.repository}")
        print(f"\targs: {self.args}")
