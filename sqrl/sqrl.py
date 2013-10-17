#!/usr/bin/env python

# TODO Catch connection errors
# TODO Catch sqrlurl format errors
# TODO Add logging option
# TODO Standardize masterkey storage location

"""
Usage: sqrl [-d] [-n] [--path=<Dir>] <SQRLURL>

Options:
  -d               Debugging output
  -n               Notify via libnotify (Gnome)
  -p --path=<Dir>  Path for config and key storage

Example:
    sqrl "sqrl://example.com/login/sqrl?d=6&nut=a95fa8e88dc499758"
"""

import os
from .mkm import MKM
from client import Client
from docopt import docopt

VERSION = "0.0.2"
HOME = os.environ['HOME']
CONFIG_DIR = '.config/sqrl/'
WORKING_DIR = HOME + '/' + CONFIG_DIR


def main():
    arguments = docopt(__doc__, version=VERSION)
    url = arguments.get('<SQRLURL>')
    bool_notify = arguments.get('-n')
    path = arguments.get('--path')
    debug = arguments.get('-d')

    if not path:
        path = WORKING_DIR

    if not debug:
        debug = False

    run(url, path, debug, bool_notify)


def run(url, path, debug, bool_notify=False):
    # Get MasterKey
    manager = MKM(path)
    masterkey = manager.get_key()

    # Create sqrl client and submit request
    sqrlclient = Client(masterkey, url, bool_notify, debug)
    sqrlclient.submit()

if __name__ == "__main__":
    main()
