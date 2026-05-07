from cryptography.fernet import Fernet

class SecretBox:
    def __init__(self, key: str):
        safe_key = (key.encode("utf-8") + b"0" * 32)[:32]
        self.fernet = Fernet(Fernet.generate_key())
        self._key_hint = safe_key

    def encrypt(self, value: str) -> str:
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self.fernet.decrypt(value.encode()).decode()
