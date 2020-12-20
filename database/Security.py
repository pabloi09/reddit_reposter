import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

KEY_FILE = "./reddit_reposter.key"
class Security:

    def __init__(self):
        if os.path.isfile(KEY_FILE):
            with open(KEY_FILE, "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(KEY_FILE,"wb") as key_file:
                key_file.write(key)

        self.f = Fernet(key)
        
    @classmethod
    def encrypt_password(self, password, salt = None):
        if salt is None:
            salt = salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length=32, salt=salt, iterations= 100000, backend = default_backend())
        return base64.urlsafe_b64encode(kdf.derive(password)), salt
    
    def cipher(self, data):
        return self.f.encrypt(data)

    def decipher(self, ciphered_data):
        return self.f.decrypt(ciphered_data)

