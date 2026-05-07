import base64
import hashlib

from cryptography.fernet import Fernet


class SecretBox:
    def __init__(self, key: str):
        digest = hashlib.sha256(key.encode("utf-8")).digest()
        fernet_key = base64.urlsafe_b64encode(digest)
        self.fernet = Fernet(fernet_key)

    def encrypt(self, value: str) -> str:
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self.fernet.decrypt(value.encode()).decode()
