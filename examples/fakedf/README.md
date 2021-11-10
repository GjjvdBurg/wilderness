# FakeDF

This is an example package that uses Wilderness to build a command line 
application without subcommands. As an example, this package mimicks the Unix 
``df`` program. See the [instructions here][instructions] on how to install 
this package.

A few aspects to note in this example:

 - The default ``help`` command is not used in this example. Help is only 
   available through the ``--help`` flag, as in ``df``. This is achieved by 
   supplying ``add_help=False`` to the ``Application`` constructor and adding 
   the ``--help`` argument separately under ``register()``.

 - The ``OPTIONS`` section in the man page has a prolog and an epilog, which 
   are supplied through the ``Application`` constructor.

 - Long documentation is kept in a separate module.

 - None of the arguments have a longer documentation string in the man page, 
   hence the ``description`` keyword of the ``add_argument`` method is not 
   used.

 - The ``run`` method of the ``FakeDFApplication`` needs to call the 
   ``super().run()`` method to parse the command line arguments.

[instructions]: https://github.com/GjjvdBurg/wilderness/tree/master/examples/
