import nacl.utils
import nacl.signing
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC
import base64

PRIVATE_KEY = b'2A~\xf8R\n,\r\x9b(\x0b\xc6\xd9\xae\xc4\xdd\x8b\xa07\xc1O\x8b\xdfg\x7f`\xc61\xb3&\xe2\xef'

### CLIENT
def make_key(private_key, site):
	h = HMAC.new(private_key, digestmod=SHA256)
	h.update(site)
	return h.digest()

def create_code(challenge, site):
	site_key = make_key(PRIVATE_KEY, site)
	signing_key = nacl.signing.SigningKey(site_key)
	signed = signing_key.sign(challenge)
	public_key = signing_key.verify_key
	return public_key._key, signed

### SERVER
def verify_key(public_key, signature, challenge):
	vk = nacl.signing.VerifyKey(public_key)
	return challenge == vk.verify(signature)

challenge = nacl.utils.random(32)
k,m = create_code(challenge, b"www.grc.com")

t = verify_key(k, m, challenge)
print(t)
