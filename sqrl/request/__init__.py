#!/usr/bin/env python

import httplib

__sqrlver__ = "1"


class SQRLRequest():
    """
    SQRLRequestor
    - Formats SQRL request
    - Submits the SQRL reuqest
    """

    def __init__(self, uri, public_key):
        self.headers = SQRLHeader()
        self.params = SQRLParams()
        self.params.set_key(public_key)
        self.uri = uri
        self.http = httplib.HTTPConnection(self.uri.domain, timeout=9)

    def _path(self):
        res = [self.uri.path, "?", self.uri.query,
               "&", self.params.get()]
        return "".join(res)

    def url(self):
        return self.uri.domain + self._path()

    def _body(self, body):
        return "sqrlsig=" + body

    def send(self, body):
        body = self._body(body)
        path = self._path()
        self.http.request("POST", path, body, self.headers.get())
        response = self.http.getresponse()
        if response.status == 200:
            return True
        else:
            return False


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
        self.set_ver(__sqrlver__)
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
