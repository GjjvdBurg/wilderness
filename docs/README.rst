
Wilderness
==========


.. image:: https://badge.fury.io/py/wilderness.svg
   :target: https://pypi.org/project/wilderness
   :alt: PyPI version


.. image:: https://github.com/GjjvdBurg/wilderness/workflows/build/badge.svg
   :target: https://github.com/GjjvdBurg/wilderness/actions
   :alt: Build status


.. image:: https://pepy.tech/badge/wilderness
   :target: https://pepy.tech/project/wilderness
   :alt: Downloads


.. image:: https://readthedocs.org/projects/wilderness/badge/?version=latest
   :target: https://wilderness.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status



.. raw:: html

   <p align="right"><i>In wildness is the salvation of the world.</i> &mdash; 
   Aldo Leopold</p>


Wilderness is a light wrapper around `argparse <https://docs.python.org/3/library/argparse.html>`_ for creating command 
line applications with multiple subcommands, in the style of `Git <https://git-scm.com/>`_. 
Wilderness also makes it easy to generate man pages for your application.

Wilderness is heavily inspired by `Cleo <https://github.com/sdispater/cleo>`_ and 
`argparse-manpage <https://github.com/praiskup/argparse-manpage>`_\ , but aims to stick as closely as possible 
to `argparse <https://docs.python.org/3/library/argparse.html>`_ to avoid users having to learn a new API.

Installation
------------

Wilderness is available on PyPI:

.. code-block::

   $ pip install wilderness

Usage
-----

Building command line applications with Wilderness is straightforward, but it 
does expect a certain structure of the application. You can create 
applications with or without subcommands, as illustrated with the 
`fakegit <https://github.com/GjjvdBurg/wilderness/tree/master/examples/fakegit>`_ and `fakedf <https://github.com/GjjvdBurg/wilderness/tree/master/examples/fakedf>`_ examples, respectively.

Creating wilderness applications consist of the following steps:


#. 
   Subclassing the ``wilderness.Application`` class to hold the main 
   application.

#. 
   Adding one or more ``wilderness.Command`` objects for each of the 
   subcommands, optionally organized into ``wilderness.Group``\ s.

#. 
   Minor changes to ``setup.py`` to build the manpages.

Examples
--------

Here are some examples that use Wilderness to build command line applications:

.. list-table::
   :header-rows: 1

   * - Repository
     - Description
   * - `fakegit <https://github.com/GjjvdBurg/wilderness/tree/master/examples/fakegit>`_
     - A multi-level command line application similar to Git
   * - `fakedf <https://github.com/GjjvdBurg/wilderness/tree/master/examples/fakedf>`_
     - An application without subcommands similar to df
   * - `CleverCSV <https://github.com/alan-turing-institute/CleverCSV>`_
     - CleverCSV is a package for handling messy CSV files
   * - `Veld <https://github.com/GjjvdBurg/Veld/>`_
     - Easy command line analytics


..

   Add your example here by opening a pull request!


Notes
-----

License: See the LICENSE file.

Author: `Gertjan van den Burg <https://gertjanvandenburg.com>`_
