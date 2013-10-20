#!/usr/bin/env python

import httplib
from sqrl.test import test

__sqrlver__ = "1"


class SQRLRequest():
    """
    SQRLRequest
    - Formats SQRL request
    - Submits the SQRL reuqest
    """

    def __init__(self, url, public_key):
        self.headers = SQRLHeader()

        self.params = SQRLParams()
        self.params.set_key(public_key)
        self.params.set_ver(__sqrlver__)
        self.key = public_key

        self.url = url
        if self.url.isSecure():
            self.http = httplib.HTTPSConnection(self.url.netloc, timeout=9)
        else:
            self.http = httplib.HTTPConnection(self.url.netloc, timeout=9)

    def _path(self):
        res = [self.url.path, "?", self.url.query,
               "&", self.params.get()]
        return "".join(res)

    def get_url(self):
        return self.url.scheme + "://" + self.url.netloc + self._path()

    def _body(self, body):
        return "sqrlsig=" + body

    def send(self, body, debug):
        sigbody = self._body(body)
        path = self._path()
        try:
            self.http.request("POST", path, sigbody, self.headers.get())
            response = self.http.getresponse()
        except Exception as e:
            code, msg = e
            print (msg)
            return False, msg

        # Display debug info if set
        if debug:
            test(self.get_url(), body,
                 self.key, self.url.domain, __sqrlver__)

        if response.status == 200:
            return True, "Authentication Successful!"
        else:
            return False, "Authentication Failed! " + response.reason


class SQRLHeader:
    """
    SQRLHeader
    """
    def __init__(self):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain"}

    def get(self):
        return self.headers


class SQRLParams:
    """
    SQRLParam
    - Builds out the parameters specific to SQRL
    - Formats and checks each param
    """
    def __init__(self):
        self.buffer = []
        self.set = ""
        self.key = ""
        self.opt = []

    def set_ver(self, ver):
        self.ver = "sqrlver=" + ver

    def set_key(self, key):
        self.key = "sqrlkey=" + key

    def add_opt(self, option):
        if self.opt.length == 0:
            self.opt = ["sqrlopt=" + option]
        else:
            self.opt.append(option)

    def get(self):
        opts = ",".join(self.opt)
        params = filter(None, [self.ver, opts, self.key])
        result = "&".join(params)
        return result
