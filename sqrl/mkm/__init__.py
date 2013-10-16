#!/usr/bin/env python
import ed25519
import os


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
