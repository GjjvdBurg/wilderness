#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import io
import os

from distutils.core import Command

from setuptools import find_packages
from setuptools import setup

# Package meta-data.
NAME = "fakedf"
DESCRIPTION = "Fake df for testing Wilderness"
AUTHOR = "Gertjan van den Burg"
EMAIL = "gertjanvandenburg@gmail.com"
LICENSE = "MIT"
LICENSE_TROVE = "License :: OSI Approved :: MIT License"
REQUIRES_PYTHON = ">=3.6.0"
URL = ""
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = ["wilderness"]

# What packages are optional?
docs_require = []
test_require = []
dev_require = []

EXTRAS = {
    "docs": docs_require,
    "test": test_require,
    "dev": dev_require + test_require + docs_require,
}


class manpages(Command):
    description = "Generate manpages"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from fakedf.console import build_application

        from wilderness import build_manpages

        build_manpages(build_application())


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    license=LICENSE,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    entry_points={"console_scripts": ["fakedf=fakedf.__main__:main"]},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    data_files=[("man/man1", glob.glob("man/*.1"))],
    cmdclass={"build_manpages": manpages},
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        LICENSE_TROVE,
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
