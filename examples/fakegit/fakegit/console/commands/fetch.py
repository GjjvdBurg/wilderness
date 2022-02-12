# -*- coding: utf-8 -*-

import argparse

from wilderness import Command


class FetchCommand(Command):
    _description = (
        'Fetch branches and/or tags (collectively, "refs") from one or '
        "more other repositories, along with the objects necessary to "
        "complete their histories. Remote-tracking branches are updated "
        "(see the description of <refspec> below for ways to control "
        "this behavior)."
        "\n"
        "By default, any tag that points into the histories being "
        "fetched is also fetched; the effect is to fetch tags that point "
        "at branches that you are interested in. This default behavior "
        "can be changed by using the --tags or --no-tags options or by "
        "configuring remote.<name>.tagOpt. By using a refspec that "
        "fetches tags explicitly, you can fetch tags that do not point "
        "into branches you are interested in as well."
    )

    def __init__(self):
        super().__init__(
            name="fetch",
            title="Download objects and refs from another repository",
            description=self._description,
        )

    def register(self):
        self.add_argument(
            "repository",
            help=argparse.SUPPRESS,
            description=(
                'The "remote" repository that is the source of a fetch or '
                "pull operation. This parameter can be either a URL (see the "
                "section GIT URLS below) or the name of a remote (see the "
                "section REMOTES below)."
            ),
        )

    def handle(self):
        print("Running git fetch, repository=%s" % self.args.repository)
