#!/usr/bin/env python

from urlparse import urlparse
from urlparse import parse_qs


class URLParser():
    """
    URLParser
    - Value object for initial SQRL URL
    """

    def __init__(self, uri):
        self.orig_uri = uri
        uri_parsed = urlparse(uri)
        self._validate(uri_parsed)
        self._processURI(uri_parsed)

    def _validate(self, uri_parsed):
        if uri_parsed.scheme not in ["sqrl", "qrl"]:
            self._cancel("Bad Scheme")

        if uri_parsed.netloc is "":
            self._cancel("No Domain")

        if uri_parsed.path is "":
            self._cancel("Invalid Path")

        if uri_parsed.query is "":
            self._cancel("No Query String")

    def _cancel(self, msg):
        pass

    def _processURI(self, uri):
        self.domain = uri.netloc
        self.path = uri.path
        self.scheme = uri.scheme
        self.query = uri.query
        self.queries = parse_qs(uri.query)

    def getURI(self):
        return self.orig_uri

    def getDomain(self):
        domain = ''
        if "d" in self.queries:
            depth = int(self.queries['d'][0])
            domain = self.domain + self.path[0:depth]
        else:
            domain = self.domain
        return domain
