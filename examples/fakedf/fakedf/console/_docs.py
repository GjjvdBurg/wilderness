# -*- coding: utf-8 -*-

DOCS = {
    "description": (
        "This manual page documents the GNU version of df. df displays the "
        "amount of space available on the file system containing each file "
        "name argument. If no file name is given, the space available on "
        "all currently mounted file systems is shown. Space is shown in 1K "
        "blocks by default, unless the environment variable POSIXLY_CORRECT "
        "is set, in which case 512-byte blocks are used."
        "\n\n"
        "If an argument is the absolute file name of a device node "
        "containing a mounted file system, df shows the space available on "
        "that file system rather than on the file system containing the "
        "device node. This version of df cannot show the space available "
        "on unmounted file systems, because on most kinds of systems doing "
        "so requires very nonportable intimate knowledge of file system "
        "structures."
    ),
    "extra": {
        "author": (
            "Written by Torbjorn Granlund, David MacKenzie, and Paul Eggert."
        ),
        "Reporting Bugs": (
            "GNU coreutils online help: "
            "<https://www.gnu.org/software/coreutils/>\n"
            "Report any translation bugs to "
            "<https://translationproject.org/team/>"
        ),
        "Copyright": (
            "Copyright © 2021 Free Software Foundation, Inc. License GPLv3+: "
            "GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.\n"
            "This is free software: you are free to change and redistribute "
            "it. There is NO WARRANTY, to the extent permitted by law."
        ),
        "See also": (
            "Full documentation <https://www.gnu.org/software/coreutils/df> "
            "or available locally via: info '(coreutils) df invocation'"
        ),
    },
    "options": {
        "prolog": (
            "Show information about the file system on which each FILE "
            "resides, or all file systems by default.\n\n"
            "Mandatory arguments to long options are mandatory for short "
            "options too."
        ),
        "epilog": (
            "Display values are in units of the first available SIZE from "
            "--block-size, and the DF_BLOCK_SIZE, BLOCK_SIZE and BLOCKSIZE "
            "environment variables. Otherwise, units default to 1024 bytes "
            "(or 512 if POSIXLY_CORRECT is set)."
            "\n\n"
            "The SIZE argument is an integer and optional unit (example: "
            "10K is 10*1024). Units are K,M,G,T,P,E,Z,Y (powers of 1024) or "
            "KB,MB,... (powers of 1000). Binary prefixes can be used, too: "
            "KiB=K, MiB=M, and so on."
            "\n\n"
            "FIELD_LIST is a comma-separated list of columns to be "
            "included. Valid field names are: 'source', 'fstype', 'itotal', "
            "'iused', 'iavail', 'ipcent', 'size', 'used', 'avail', 'pcent', "
            "'file' and 'target' (see info page)."
        ),
    },
    "footer": (
        "GNU coreutils online help: "
        "<https://www.gnu.org/software/coreutils/>\n"
        "Full documentation <https://www.gnu.org/software/coreutils/df>\n"
        "or available locally via: info '(coreutils) df invocation'"
    ),
}
