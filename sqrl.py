import nacl.utils
import nacl.signing

import hashlib
import hmac
import base64
import urllib.parse

class Client:
    def __init__(self, private_key):
        self.private_key = private_key

    def make_key(self, site):
        h = hmac.new(self.private_key, digestmod=hashlib.sha256)
        h.update(bytes(site, "utf-8"))
        return h.digest()

    def create_code(self, sqrl):
        parsed = urllib.parse.urlparse(sqrl)
        site = parsed.netloc
        encoded = urllib.parse.parse_qs(parsed.query)["sqrl"][0]
        
        challenge = base64.urlsafe_b64decode(encoded)
        site_key = self.make_key(site)
        signing_key = nacl.signing.SigningKey(site_key)
        signed = signing_key.sign(bytes(challenge))
        public_key = signing_key.verify_key
        return public_key._key, signed

class ServerSession:
    def __init__(self, site):
        self.challenge = nacl.utils.random(32)
        self.site = site

    def get_sqrl(self):
        return "sqrl://{}?sqrl={}".format(self.site,str(base64.urlsafe_b64encode(self.challenge), "utf-8"))

    def verify_key(self, public_key, signature):
        vk = nacl.signing.VerifyKey(public_key)
        try:
            out = vk.verify(signature)
        except nacl.signing.BadSignatureError:
            return False
        return self.challenge == out


if __name__ == "__main__":

    # These are of course supposed to be chosen with a good RNG but for this test-case it doesn't matter
    PRIVATE_KEY1 = b'correct horse battery staple' 
    PRIVATE_KEY2 = b'wrong horse battery staple'

    client1 = Client(PRIVATE_KEY1)
    client2 = Client(PRIVATE_KEY2)

    session = ServerSession("www.grc.com")
    sqrl_url = session.get_sqrl()

    print (sqrl_url)

    k1, m1 = client1.create_code(sqrl_url)
    k2, m2 = client2.create_code(sqrl_url)

    print("Verifying client1: ", session.verify_key(k1, m1))
    print("Verifying client2: ", session.verify_key(k2, m2))
    print("Verifying bad key: ", session.verify_key(k1, m2))
