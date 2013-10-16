#!/usr/bin/env python

import base64


class baseconv:
    """
    BaseConverter
    Uitility to encode and decode base64url to spec
    """

    @classmethod
    def cleanUp(self, value):
        while value[-1] == "=":
            value = value.rstrip("=")
        return value

    @classmethod
    def decode(self, value):
        value = base64.urlsafe_b64decode(value)
        return self.cleanUp(value)

    @classmethod
    def encode(self, value):
        value = base64.urlsafe_b64encode(value)
        return self.cleanUp(value)
