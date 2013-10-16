#!/usr/bin/env python

# TODO Add notification feature to documentation
# TODO Catch connection errors
# TODO Catch sqrlurl format errors
# TODO Separate components to their own modules
# TODO Add logging option
# TODO Standardize masterkey storage location

"""
Usage: sqrl [-n] <SQRLURL>

-n      Notify via libnotify (Gnome)

Example:
    sqrl "sqrl://example.com/login/sqrl?d=6&nut=a95fa8e88dc499758"
"""

from client import Client
from .mkm import MKM
from docopt import docopt

VERSION = "0.0.2"


def main():
    arguments = docopt(__doc__, version=VERSION)
    url = arguments.get('<SQRLURL>')
    bool_notify = arguments.get('-n')
    run(url, bool_notify)


def run(url, bool_notify=False):
    # Get MasterKey
    manager = MKM()
    masterkey = manager.get_key()

    # Create sqrl client and submit request
    sqrlclient = Client(masterkey, url, bool_notify)
    sqrlclient.submit()

if __name__ == "__main__":
    main()
