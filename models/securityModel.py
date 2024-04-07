from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import json
import uuid
import base64
import os

class SecurityModel:
    def __init__(self, encryption_key_base64, **kwargs):
        self.backend = default_backend()
        encryption_key = base64.urlsafe_b64decode(encryption_key_base64)
        self.encryption_key = encryption_key.ljust(32, b'\0')[:32]
        self.cipher = Cipher(algorithms.AES(self.encryption_key), modes.ECB(), backend=self.backend)
        self.stage = os.environ.get('STAGE', 'dev').lower()
        if '_id' not in kwargs:
            self._id = str(uuid.uuid4())
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _pad(self, data_bytes):
        padding_length = 16 - len(data_bytes) % 16
        padding = bytes([padding_length] * padding_length)
        return data_bytes + padding

    def _unpad(self, data_bytes):
        padding_length = data_bytes[-1]
        return data_bytes[:-padding_length]

    def encrypt_string(self, plaintext_string):
        if self.stage == 'dev':
            return plaintext_string

        encryptor = self.cipher.encryptor()
        plaintext_bytes = plaintext_string.encode('utf-8')
        padded_data = self._pad(plaintext_bytes)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        encrypted_data_base64 = base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        return encrypted_data_base64

    def decrypt_string(self, encrypted_string):
        if self.stage == 'dev':
            return encrypted_string

        decryptor = self.cipher.decryptor()
        encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_string)
        decrypted_data = decryptor.update(encrypted_data_bytes) + decryptor.finalize()
        unpadded_data_bytes = self._unpad(decrypted_data)
        return unpadded_data_bytes.decode('utf-8')

    @classmethod
    def from_dict(cls, encryption_key_base64, data):
        """
        The 'SecurityModel' class provides encryption and decryption functionality using the AES algorithm.

        Attributes:
            backend (cryptography.hazmat.backends.Backend): The backend used for cryptographic operations.
            encryption_key (bytes): The encryption key used for AES encryption.
            cipher (cryptography.hazmat.primitives.ciphers.Cipher): The cipher object used for encryption and decryption.
            stage (str): The stage of the application (e.g., 'dev', 'prod').

        Methods:
            __init__(self, encryption_key_base64, **kwargs): Initializes the SecurityModel object with the provided encryption key and optional keyword arguments.
            _pad(self, data_bytes): Pads the given data bytes with PKCS7 padding.
            _unpad(self, data_bytes): Removes the PKCS7 padding from the given data bytes.
            encrypt_string(self, plaintext_string): Encrypts the given plaintext string using AES encryption.
            decrypt_string(self, encrypted_string): Decrypts the given encrypted string using AES decryption.
            from_dict(cls, encryption_key_base64, data): Creates a SecurityModel object from a dictionary, decrypting the values if necessary.
            to_dict(self): Converts the SecurityModel object to a dictionary, encrypting the values if necessary.
            encrypt_dict(self, data_dict): Encrypts the string values in a dictionary.
            decrypt_dict(self, encrypted_dict): Decrypts the string values in a dictionary.
        """
        instance = cls(encryption_key_base64)
        decrypted_data = {}
        for k, v in data.items():
            if isinstance(v, str):
                decrypted_value = instance.decrypt_string(v)
                decrypted_data[k] = decrypted_value
            else:
                decrypted_data[k] = v
        for key, value in decrypted_data.items():
            setattr(instance, key, value)
        return instance

    def to_dict(self):
        encrypted_data = {}
        """
        The 'SecurityModel' class provides encryption and decryption functionality using the AES algorithm.

        Attributes:
            backend (cryptography.hazmat.backends.Backend): The backend used for cryptographic operations.
            encryption_key (bytes): The encryption key used for AES encryption.
            cipher (cryptography.hazmat.primitives.ciphers.Cipher): The cipher object used for encryption and decryption.
            stage (str): The stage of the application (e.g., 'dev', 'prod').

        Methods:
            __init__(self, encryption_key_base64, **kwargs): Initializes the SecurityModel object with the provided encryption key and optional keyword arguments.
            _pad(self, data_bytes): Pads the given data bytes with PKCS7 padding.
            _unpad(self, data_bytes): Removes the PKCS7 padding from the given data bytes.
            encrypt_string(self, plaintext_string): Encrypts the given plaintext string using AES encryption.
            decrypt_string(self, encrypted_string): Decrypts the given encrypted string using AES decryption.
            from_dict(cls, encryption_key_base64, data): Creates a SecurityModel object from a dictionary, decrypting the values if necessary.
            to_dict(self): Converts the SecurityModel object to a dictionary, encrypting the values if necessary.
            encrypt_dict(self, data_dict): Encrypts the string values in a dictionary.
            decrypt_dict(self, encrypted_dict): Decrypts the string values in a dictionary.
        """
        for k, v in self.__dict__.items():
            if k not in ['encryption_key', 'cipher', 'backend','stage']:
                if isinstance(v, str):
                    encrypted_value = self.encrypt_string(v) if self.stage in ['prod', 'production'] else v
                    encrypted_data[k] = encrypted_value
                else:
                    encrypted_data[k] = v
        return encrypted_data

    def encrypt_dict(self, data_dict):
        """
        Chiffre les valeurs de chaînes dans un dictionnaire.
        """
        encrypted_data = {}
        for k, v in data_dict.items():
            # Chiffre uniquement les chaînes de caractères
            if isinstance(v, str):
                encrypted_value = self.encrypt_string(v)
                encrypted_data[k] = encrypted_value
            else:
                # Laisse les autres types de données inchangés
                encrypted_data[k] = v
        return encrypted_data

    def decrypt_dict(self, encrypted_dict):
        """
        Déchiffre les valeurs de chaînes dans un dictionnaire.
        """
        decrypted_data = {}
        for k, v in encrypted_dict.items():
            # Déchiffre uniquement les valeurs qui sont des chaînes de caractères
            if isinstance(v, str):
                decrypted_value = self.decrypt_string(v)
                decrypted_data[k] = decrypted_value
            else:
                # Laisse les autres types de données inchangés
                decrypted_data[k] = v
        return decrypted_data