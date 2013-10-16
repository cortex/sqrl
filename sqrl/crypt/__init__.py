#!/usr/bin/env python

import ed25519
import hmac
from sqrl.utils import baseconv


class Crypt:
    """
    Crypt
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
        return baseconv.encode(signed)

    def getPublicKey(self):
        key = self.vk.to_bytes()
        return baseconv.encode(key)
