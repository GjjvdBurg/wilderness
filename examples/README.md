# Wilderness Examples

This directory contains a few examples of how [wilderness][wilderness] can be 
used to create command line applications with man pages.

 - FakeDF: Illustrates how to create an application without subcommands and 
   mimicks the Unix ``df`` command.

 - FakeGit: Illustrates how to create multi-level command line applications 
   with subcommands, similar to Git.

Building the examples can be done as follows, for each package:

```bash
# Build the man pages
$ python setup.py build_manpages

# Build the source and wheel distributions
$ python setup.py sdist bdist_wheel

# Install the package
$ pip install --user ./dist/*.whl
```

After that, you should be able to run the examples:

* fakedf:

  ```bash
  # Show the man page for fakedf
  $ man fakedf

  # Show the help
  $ fakedf --help
  ```

* fakegit:

  ```bash
  # Show the man page for fakegit
  $ man fakegit

  # Show the man page for a subcommand
  $ fakegit help clone

  # Show the help for the application
  $ fakegit

  # Show short help for a subcommand
  $ fakegit init -h
  ```

[wilderness]: https://github.com/GjjvdBurg/wilderness
