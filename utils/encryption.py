from __future__ import annotations

import base64

from config import SECRET_KEY
from config import IV

from crypto.Cipher import AES


def encrypt(value):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    padded_value = value + (16 - len(value) % 16) * chr(16 - len(value) % 16)
    encrypted_value = cipher.encrypt(padded_value.encode())
    encoded_value = base64.b64encode(encrypted_value).decode()
    return encoded_value


def decrypt(encoded_value):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    encrypted_value = base64.b64decode(encoded_value.encode())
    decrypted_value = cipher.decrypt(encrypted_value).decode()
    unpadded_value = decrypted_value[:-ord(decrypted_value[-1])]
    return unpadded_value