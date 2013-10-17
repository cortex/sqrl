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

    def __init__(self, masterkey):
        self.masterkey = masterkey

    def _site_key_pair(self, domain):
        seed = self._site_seed(domain)
        sk = ed25519.SigningKey(seed)
        vk = sk.get_verifying_key()
        return sk, vk

    def _site_seed(self, domain):
        """
        Generates a seed to based on the masterkey
        and the current site you authenicating with
        The seed is used to generate the key pair
        used for signing the request body
        """
        key = self.masterkey
        local_hmac = hmac.new(key)
        local_hmac.update(domain)
        return local_hmac.hexdigest()

    def sign(self, value):
        signed = self.sk.sign(value)
        return baseconv.encode(signed)

    def getPublicKey(self, domain):
        self.sk, self.vk = self._site_key_pair(domain)
        key = self.vk.to_bytes()
        return baseconv.encode(key)
