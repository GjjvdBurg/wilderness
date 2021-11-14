# Wilderness

[![PyPI version](https://badge.fury.io/py/wilderness.svg)](https://pypi.org/project/wilderness)
[![Build status](https://github.com/GjjvdBurg/wilderness/workflows/build/badge.svg)](https://github.com/GjjvdBurg/wilderness/actions)
[![Downloads](https://pepy.tech/badge/wilderness)](https://pepy.tech/project/wilderness)
[![Documentation Status](https://readthedocs.org/projects/wilderness/badge/?version=latest)](https://wilderness.readthedocs.io/en/latest/?badge=latest)

Wilderness is a light wrapper around [argparse][argparse] for creating command 
line applications with multiple subcommands, in the style of [Git][git]. 
Wilderness also makes it easy to generate man pages for your application.

Wilderness is heavily inspired by [Cleo][cleo] and 
[argparse-manpage][argparse-manpage], but aims to stick as closely as possible 
to [argparse][argparse] to avoid users needing to learn a new API.

## Installation

Wilderness is available on PyPI:

```
$ pip install wilderness
```

## Usage

Building command line applications with Wilderness is straightforward, but it 
does expect a certain structure of the application. You can create 
applications with or without subcommands, as illustrated with the 
[fakedf][fakedf] and [fakegit][fakegit] examples, respectively.

Creating wilderness applications consist of the following steps:

1. Subclassing the ``wilderness.Application`` class to hold the main 
   application.

2. Adding one or more ``wilderness.Command`` objects for each of the 
   subcommands, optionally organized into ``wilderness.Group``s.

3. Minor changes to ``setup.py`` to build the manpages.

## Examples

Here are some examples that use Wilderness to build command line applications:

| Repository | Description |
|------------|-------------|
| [fakegit][fakegit] | A multi-level command line application similar to Git |
| [fakedf][fakedf] | An application without subcommands similar to df |

> Add your example here by opening a pull request!

## Notes

License: See the LICENSE file.

Author: [Gertjan van den Burg][gertjan]

[argparse-manpage]: https://github.com/praiskup/argparse-manpage
[argparse]: https://docs.python.org/3/library/argparse.html
[cleo]: https://github.com/sdispater/cleo
[fakedf]: https://github.com/GjjvdBurg/wilderness/tree/master/examples/fakedf
[fakegit]: https://github.com/GjjvdBurg/wilderness/tree/master/examples/fakegit
[gertjan]: https://gertjanvandenburg.com
[git]: https://git-scm.com/
