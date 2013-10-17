#!/usr/bin/env python

import pynotify
from crypt import Crypt
from parser import URLParser
from request import SQRLRequest


class Client:
    def __init__(self, masterkey, url, notice=False):
        self.parser = URLParser(url)
        self.domain = self.parser.getDomain()
        self.notice = notice
        enc = Crypt(masterkey)
        public_key = enc.getPublicKey(self.domain)
        self.sqrlreq = SQRLRequest(self.parser, public_key)
        unsigned_url = self.sqrlreq.url()
        self.signed_url = enc.sign(unsigned_url)

    def _notify(self, msg):
        if self.notice:
            pynotify.init("SQRL")
            n = pynotify.Notification("pySQRL", msg)
            n.show()

    def submit(self):
        result = self.sqrlreq.send(self.signed_url)

        # notify of server response
        if result:
            self._notify("Authentication to " + self.domain + ": Successful")
        else:
            self._notify("Authentication to " + self.domain + ": Failed")
