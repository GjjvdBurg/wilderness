#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import io
import os

from fakegit.console import build_application
from setuptools import find_packages
from setuptools import setup

from wilderness import manpage_builder

# Package meta-data.
AUTHOR = "Gertjan van den Burg"
DESCRIPTION = "Fake Git for testing Wilderness"
EMAIL = "gertjanvandenburg@gmail.com"
LICENSE = "MIT"
LICENSE_TROVE = "License :: OSI Approved :: MIT License"
NAME = "fakegit"
REQUIRES_PYTHON = ">=3.6.0"
URL = ""
VERSION = None

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
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    install_requires=[],
    extras_require={},
    include_package_data=True,
    license=LICENSE,
    ext_modules=[],
    data_files=[("man/man1", glob.glob("man/*.1"))],
    cmdclass={"build_manpages": manpage_builder(build_application())},
    entry_points={"console_scripts": ["fakegit=fakegit.__main__:main"]},
)
