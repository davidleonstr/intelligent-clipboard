import random

class SeedCipher:
    'Seed cipher helper.'
    def __init__(self, seed: str):
        self.seed = seed

    def _get_keystream(self, length: int):
        random.seed(self.seed)
        return [random.randint(0, 255) for _ in range(length)]

    def encrypt(self, text: str) -> bytes:
        data = text.encode('utf-8')
        keystream = self._get_keystream(len(data))

        encrypted = bytes([b ^ k for b, k in zip(data, keystream)])
        return encrypted

    def decrypt(self, encrypted: bytes) -> str:
        keystream = self._get_keystream(len(encrypted))

        decrypted = bytes([b ^ k for b, k in zip(encrypted, keystream)])
        return decrypted.decode('utf-8')