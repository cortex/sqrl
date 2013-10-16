#!/usr/bin/env python

import ed25519
from .utils import baseconv


def test(uri, signed_uri, public_key, domain):
    """
    Verifies the components of the challenge for debugging
    """

    key = baseconv.decode(public_key + "==")
    verifying_key = ed25519.VerifyingKey(key)

    print "URI: " + uri
    print "Domin: \"" + domain + "\""
    print "Publick Key: " + public_key
    print "Signed URI: " + signed_uri
    try:

        signed_uri = baseconv.decode(signed_uri + "==")
        verifying_key.verify(signed_uri, uri)
        print "signature is good"
    except ed25519.BadSignatureError:
        print "signature is bad!"
