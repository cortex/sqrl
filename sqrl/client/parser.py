#!/usr/bin/env python

from urlparse import urlparse
from urlparse import parse_qs


class URLParser():
    """
    URLParser
    - Value object for initial SQRL URL
    """

    def __init__(self, url):
        self.orig_url = url
        url_parsed = urlparse(url)
        self._validate(url_parsed)
        self._processurl(url_parsed)

    def _validate(self, url_parsed):
        if url_parsed.scheme not in ["sqrl", "qrl"]:
            self._cancel("Bad Scheme")

        if url_parsed.netloc is "":
            self._cancel("No Domain")

        if url_parsed.path is "":
            self._cancel("Invalid Path")

        if url_parsed.query is "":
            self._cancel("No Query String")

    def _cancel(self, msg):
        pass

    def _processurl(self, url):
        self.domain = self._cleanDomain(url.netloc)
        self.netloc = url.netloc
        self.path = url.path
        self.scheme = url.scheme
        self.query = url.query
        self.queries = parse_qs(url.query)

    def getURL(self):
        return self.orig_url

    def _cleanDomain(self, domain):
        return domain.split(":")[0]

    def getDomain(self):
        domain = ''
        if "d" in self.queries:
            depth = int(self.queries['d'][0])
            domain = self.domain + self.path[0:depth]
        else:
            domain = self.domain
        return domain
