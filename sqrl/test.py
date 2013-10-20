#!/usr/bin/env python

import ed25519
from .utils import baseconv


def test(url, signed_url, public_key, domain, version):
    """
    Verifies the components of the challenge for debugging
    """

    key = baseconv.decode(public_key + "==")
    verifying_key = ed25519.VerifyingKey(key)

    print "Challenge: " + url
    print "Domin: \"" + domain + "\""
    print "SQRLver: " + version
    print "SQRLKey: " + public_key
    print "SQRLsig: " + signed_url
    try:

        signed_url = baseconv.decode(signed_url + "==")
        verifying_key.verify(signed_url, url)
        print "signature is good"
    except ed25519.BadSignatureError:
        print "signature is bad!"
