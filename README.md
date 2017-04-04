Console to Web
==============

This is a webserver that exposes a console program to users on the web. If
you have ever written a console based program that you wish people could play
around with, without giving them the code or requiring them to have any terminal
knowledge, this might help.

The interface is... minimal and a little ugly. Help in improving this would be
appreciated.

Subproceses must flush their stdout before reading from stdin.  See the example
for details.

To use, simply run

    $ python main.py examples/example

or

    $ python main.py "python examples/example"

### Caution

This works:

    $ python main.py "ps aux"

Be careful what you expose via the web.

Supported features
------------------

 * Multiple sessions
 * ANSI SGR forground colour and boldness codes

Sample
------

Clone the repository and run

    python main.py examples/example

Code style
----------

This is hacky code. Help in cleaning it up and adding features would be
appreciated.
