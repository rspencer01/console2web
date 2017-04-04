Console to Web
==============

This is a webserver that exposes a console program to users on the web. If
you have ever written a console based program that you wish people could play
around with, without giving them the code or requiring them to have any terminal
knowledge, this might help.

At the moment, it only works to serve a python program with a `main` function.
That is, you write a module that looks like this:

    import sys

    def main():
        print "Hello, there!"
        name = raw_input("Name: ")
        print "Nice to meet you, {}".format(name)
    
    if __name__ == "__main__":
        main()

As you can see, this is a fairly typical python program. If we call this
`greet.py`, then running the server, pointing to `path/to/program/greet`, it
will render a webpage allowing the user to interact with the program, pretty
much as if it were running in the console for them.

The interface is... minimal and a little ugly. Help in improving this would be
appreciated.

Supported features
------------------

 * Multiple sessions should work (but is not tested)
 * ANSI SGR forground colour and boldness codes

Wishlist
--------

* Arbitrary console programs. There is no need to limit ourselves to python
  code, if we can just override stdin and stdout for them.

Sample
------

Clone the repository and run

    python main.py examples/example

Code style
----------

This is hacky code. Help in cleaning it up and adding features would be
appreciated.
