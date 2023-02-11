
Changelog
=========

Version 0.1.9
-------------


* Add MANIFEST.in file to package for more complete packaging (thanks to 
  @martin-kokos)

Version 0.1.8
-------------


* Fix for running unit tests without man-db (GH-5)

Version 0.1.7
-------------


* Add option to automatically generate list of commands in Application manpage
* Fix support for tab indentation in man pages
* Add helpful errors when description is not of type str
* Some minor fixes

Version 0.1.6
-------------


* Bugfix for application testing
* Minor fixes for documentation of single-command applications
* Improve test discovery (GH-2)

Version 0.1.5
-------------


* Bugfix for synopsis of commands with mutually exclusive argument groups

Version 0.1.4
-------------


* Add support for mutually exclusive argument groups
* Typos and fixes

Version 0.1.3
-------------


* Add Tester class to test applications and commands
* Subclass ArgumentParser to handle exit on error
* Removed ``application.get_argument`` method
* Several smaller fixes and design improvements

Version 0.1.2
-------------


* Redesign manpage building api
* Use application help instead of manpage with ``<app> help``

Version 0.1.1
-------------


* Add py.typed file for PEP 561.
* Update help action for application
* Minor fixes

Version 0.1.0
-------------


* Initial release
