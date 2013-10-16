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

import pynotify
from .test import test
from .crypt import Crypt
from .mkm import MKM
from .request import SQRLRequest
from .parser import URLParser
from docopt import docopt

VERSION = "0.0.2"


def main():
    arguments = docopt(__doc__, version=VERSION)
    url = arguments.get('<SQRLURL>')
    bool_notify = arguments.get('-n')
    run(url, bool_notify)


def run(url, bool_notify=False):
    # Parse url
    urlparsed = URLParser(url)
    domain = urlparsed.getDomain()

    # Get MasterKey
    manager = MKM()
    masterkey = manager.get_key()

    # Generate Site Specific Key pair
    enc = Crypt(masterkey, domain)
    public_key = enc.getPublicKey()

    # Create Request Object
    sqrlreq = SQRLRequest(urlparsed, public_key)
    url = sqrlreq.url()

    # Sign the url and send it
    signed_url = enc.sign(url)
    test(url, signed_url, public_key, domain)
    result = sqrlreq.send(signed_url)

    # notify of server response
    if bool_notify:
        if result:
            notify("Authentication to " + domain + ": Successful")
        else:
            notify("Authentication to " + domain + ": Failed")


def notify(msg):
    pynotify.init("SQRL")
    n = pynotify.Notification("pySQRL", msg)
    n.show()


if __name__ == "__main__":
    main()
