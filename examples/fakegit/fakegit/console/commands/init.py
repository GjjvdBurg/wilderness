# -*- coding: utf-8 -*-

import argparse

from wilderness.command import Command


class InitCommand(Command):

    _description = (
        "This command creates an empty Git repository - basically a .git "
        "directory with subdirectories for objects, refs/heads, refs/tags, "
        "and template files. An initial branch without any commits will be "
        "created (see the --initial-branch option below for its name)."
        "\n\n"
        "If the $GIT_DIR environment variable is set then it specifies a "
        "path to use instead of ./.git for the base of the repository."
        "\n\n"
        "If the object storage directory is specified via the "
        "$GIT_OBJECT_DIRECTORY environment variable then the sha1 "
        "directories are created underneath - otherwise the default "
        "$GIT_DIR/objects directory is used."
        "\n\n"
        "Running git init in an existing repository is safe. It will not "
        "overwrite things that are already there. The primary reason for "
        "rerunning git init is to pick up newly added templates (or to move "
        "the repository to another place if --separate-git-dir is given)."
    )

    _doc_template_dir = (
        "Files and directories in the template directory whose name do not "
        "start with a dot will be copied to the $GIT_DIR after it is created."
        "\n\n"
        "The template directory will be one of the following (in order):"
        "\n\n"
        "* the argument given with the --template option;\n"
        "* the contents of the $GIT_TEMPLATE_DIR environment variable;\n"
        "* the init.templateDir configuration variable; or\n"
        "* the default template directory: /usr/share/git-core/templates.\n"
        "\n"
        "The default template directory includes some directory structure, "
        'suggested "exclude patterns" (see gitignore(5)), and sample hook '
        "files."
        "\n\n"
        "The sample hooks are all disabled by default. To enable one of the "
        "sample hooks rename it by removing its .sample suffix."
        "\n\n"
        "See githooks(5) for more general info on hook execution."
    )
    _doc_examples = (
        "Start a new Git repository for an existing code base"
        "\n\n"
        "\t$ cd /path/to/my/codebase\n"
        "\t$ git init      (1)\n"
        "\t$ git add .     (2)\n"
        "\t$ git commit    (3)\n"
        "\n"
        "1. Create a /path/to/my/codebase/.git directory.\n"
        "2. Add all existing files to the index.\n"
        "3. Record the pristine state as the first commit in the history.\n"
    )

    def __init__(self):
        super().__init__(
            name="init",
            title=(
                "Create an empty Git repository or reinitialize an "
                "existing one"
            ),
            description=self._description,
            extra_sections={
                "template directory": self._doc_template_dir,
                "examples": self._doc_examples,
                "fakegit": "Part of the fakegit(1) suite",
            },
            add_help=False,
        )

    def register(self):
        self.add_argument(
            "-h",
            "--help",
            action="help",
            help="show this help message and exit",
            description=argparse.SUPPRESS,
        )
        self.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="be quiet",
            description=(
                "Only print error and warning messages; all other output "
                "will be suppressed."
            ),
        )
        self.add_argument(
            "--bare",
            action="store_true",
            help="create a bare repository",
            description=(
                "Create a bare repository. If GIT_DIR environment is not set, "
                "it is set to the current working directory."
            ),
        )
        self.add_argument(
            "--object-format",
            help="specify the hash algorithm to use",
            metavar="<hash>",
            description=(
                "Specify the given object format (hash algorithm) for the "
                "repository. The valid values are sha1 and (if enabled) "
                "sha256. sha1 is the default."
                "\n\n"
                "THIS OPTION IS EXPERIMENTAL! SHA-256 support is experimental "
                "and still in an early stage. A SHA-256 repository will in "
                'general not be able to share work with "regular" SHA-1 '
                "repositories. It should be assumed that, e.g., Git internal "
                "file formats in relation to SHA-256 repositories may change "
                "in backwards-incompatible ways. Only use "
                "--object-format=sha256 for testing purposes."
            ),
        )
        self.add_argument(
            "--template",
            help="directory from which templates will be used",
            metavar="<template_directory>",
            description=(
                "Specify the directory from which templates will be used. "
                '(See the "TEMPLATE DIRECTORY" section below.)'
            ),
        )
        self.add_argument(
            "--separate-git-dir",
            help="separate git dir from working tree",
            metavar="<git-dir>",
            description=(
                "Instead of initializing the repository as a directory to "
                "either $GIT_DIR or ./.git/, create a text file there "
                "containing the path to the actual repository. This file "
                "acts as filesystem-agnostic Git symbolic link to the "
                "repository.\n\n"
                "If this is reinitialization, the repository will be moved "
                "to the specified path."
            ),
        )
        self.add_argument(
            "-b",
            "--initial-branch",
            help="override the name of the initial branch",
            metavar="<branch-name>",
            description=(
                "Use the specified name for the initial branch in the newly "
                "created repository. If not specified, fall back to the "
                "default name (currently master, but this is subject to "
                "change in the future; the name can be customized via the "
                "init.defaultBranch configuration variable)."
            ),
        )
        self.add_argument(
            "--shared",
            help=(
                "specify that the git repository is to be shared amongst "
                "several users"
            ),
            metavar="<permissions>",
            choices=[
                "false",
                "true",
                "umask",
                "group",
                "all",
                "world",
                "everybody",
                "0xxx",
            ],
            nargs="?",
            default="group",
            description=(
                "Specify that the Git repository is to be shared amongst "
                "several users. This allows users belonging to the same "
                "group to push into that repository. When specified, the "
                'config variable "core.sharedRepository" is set so that '
                "files and directories under $GIT_DIR are created with the "
                "requested permissions. When not specified, Git will use "
                "permissions reported by umask(2)."
                "\n\n"
                "The option can have the following values, defaulting to "
                "group if no value is given:"
                "\n\n"
                "umask (or false)\n"
                "\tUse permissions reported by umask(2). The default, when "
                "--shared is not specified."
                "\n\n"
                "group (or true)\n"
                "\tMake the repository group-writable, (and g+sx, since the "
                "git group may be not the primary group of all users). This "
                "is used to loosen the permissions of an otherwise safe "
                "umask(2) value. Note that the umask still applies to the "
                "other permission bits (e.g. if umask is 0022, using group "
                "will not remove read privileges from other (non-group) "
                "users). See 0xxx for how to exactly specify the repository "
                "permissions."
                "\n\n"
                "all (or world or everybody)\n"
                "\tSame as group, but make the repository readable by all "
                "users."
                "\n\n"
                "0xxx\n"
                "\t0xxx is an octal number and each file will have mode 0xxx. "
                "0xxx will override users' umask(2) value (and not only "
                "loosen permissions as group and all does). 0640 will create "
                "a repository which is group-readable, but not group-writable "
                "or accessible to others.  0660 will create a repo that is "
                "readable and writable to the current user and group, but "
                "inaccessible to others."
            ),
        )

        # Using argparse.SUPPRESS disables the description in the man page
        self.add_argument(
            "directory",
            help=argparse.SUPPRESS,
            nargs="?",
            default=".",
            description=argparse.SUPPRESS,
        )

    def handle(self):
        print(f"Running clone command with repository {self.args.directory}")
