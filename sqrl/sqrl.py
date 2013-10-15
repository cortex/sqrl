#!/usr/bin/env python
"""
Usage: sqrl <SQRLURL>

Example:
    sqrl.py "sqrl://example.com/login/sqrl?d=6&nut=a95fa8e88dc499758aa404fbf6a55cc8"
"""

import httplib
import hmac
import ed25519
import base64
import pynotify
import os
from docopt import docopt
from urlparse import urlparse
from urlparse import parse_qs

VERSION = "0.0.1"
SQRLVER = "1"


class URIParser():
    """
    URIParser
    - Value object for initial SQRL URL
    """

    def __init__(self, uri):
        self.orig_uri = uri
        uri_parsed = urlparse(uri)
        self._processURI(uri_parsed)

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


class MKM:
    """
    Master Key Manager
    - Creates Keys
    - Deletes Keys
    - Stores Keys and Encrypts Storage
    - Retrieves Stored Keys
    """

    def __init__(self, path="./", force=False):
        self.storageFile = path + ".secret_key"
        self.force = force
        self._create_key()

    def _create_key(self):
        sk, vk = ed25519.create_keypair()
        self._store_key(sk)

    def _store_key(self, sk):
        # if the storageFile doesnt exists or force is set write file
        if not os.path.exists(self.storageFile) or self.force:
            open(self.storageFile, "wb").write(sk.to_seed())

    def get_key(self):
        seed = open(self.storageFile, "rb").read()
        return ed25519.SigningKey(seed)


class Encryptor:
    """
    Encryptor
    - Creating site specific key pair
    - Signing SRQL response
    - Providing public key
    """

    def __init__(self, masterkey, domain):
        self.masterkey = masterkey
        self.domain = domain
        self.sk, self.vk = self._site_key_pair()

    def _site_key_pair(self):
        seed = self._site_seed()
        sk = ed25519.SigningKey(seed)
        vk = sk.get_verifying_key()
        return sk, vk

    def _site_seed(self):
        """
        Generates a seed to based on the masterkey
        and the current site you authenicating with
        The seed is used to generate the key pair
        used for signing the request body
        """
        key = self.masterkey.to_ascii(encoding="base64")
        local_hmac = hmac.new(key)
        local_hmac.update(self.domain)
        return local_hmac.hexdigest()

    def sign(self, value):
        signed = self.sk.sign(value)
        return BaseConverter.encode(signed)

    def getPublicKey(self):
        key = self.vk.to_bytes()
        return BaseConverter.encode(key)


class SQRLRequestor():
    """
    SQRLRequestor
    - Formats SQRL request
    - Submits the SQRL reuqest
    """

    def __init__(self, uri, public_key):
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain"}
        self.uri = uri
        self.key = public_key
        self.http = httplib.HTTPConnection(self.uri.domain)

    def _path(self):
        res = [self.uri.path, "?", self.uri.query,
               "&sqrlver=", SQRLVER,
               "&sqrlkey=", self.key]
        return "".join(res)

    def url(self):
        return self.uri.domain + self._path()

    def _body(self, body):
        return "sqrlsig=" + body

    def send(self, body):
        body = self._body(body)
        path = self._path()
        self.http.request("POST", path, body, self.headers)
        response = self.http.getresponse()
        if response.status == '200':
            return True
        else:
            return False


class BaseConverter:
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


def test(uri, signed_uri, public_key, domain):
    """
    Verifies the components of the challenge for debugging
    """

    key = BaseConverter.decode(public_key + "==")
    verifying_key = ed25519.VerifyingKey(key)

    print "URI: " + uri
    print "Domin: \"" + domain + "\""
    print "Publick Key: " + public_key
    print "Signed URI: " + signed_uri
    try:

        signed_uri = BaseConverter.decode(signed_uri + "==")
        verifying_key.verify(signed_uri, uri)
        print "signature is good"
    except ed25519.BadSignatureError:
        print "signature is bad!"


def main():
    arguments = docopt(__doc__, version=VERSION)
    url = arguments.get('<SQRLURL>')
    run(url)


def run(uri):
    # Parse url
    uriparsed = URIParser(uri)
    domain = uriparsed.getDomain()

    # Get MasterKey
    manager = MKM()
    masterkey = manager.get_key()

    # Generate Site Specific Key pair
    enc = Encryptor(masterkey, domain)
    public_key = enc.getPublicKey()

    # Create Request Object
    sqrlconn = SQRLRequestor(uriparsed, public_key)
    url = sqrlconn.url()

    # Sign the url and send it
    signed_url = enc.sign(url)
    #test(url, signed_url, public_key, domain)
    result = sqrlconn.send(signed_url)

    # notify of server response
    if result:
        notify("Authentication to " + domain + ": Successful")
    else:
        notify("Authentication to " + domain + ": Successful")


def notify(msg):
    pynotify.init("SQRL")
    n = pynotify.Notification("pySQRL", msg)
    n.show()


if __name__ == "__main__":
    main()
