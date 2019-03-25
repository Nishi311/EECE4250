import unittest
from cryptography.fernet import Fernet
from src.encryption.encrypt import Encryption


class ControllerTester(unittest.TestCase):
    def setup(self):
        self.key = Fernet.generate_key()

    def test_encryption(self):
        self.setup()

        test_string = "Hello World"
        encrypted_string = Encryption.encrypt_text(self.key, test_string)

        self.assertNotEqual(test_string, encrypted_string)

    def test_decryption(self):
        self.setup()

        test_string = "Hello World"
        encrypted_string = Encryption.encrypt_text(self.key, test_string)
        decrypted_string = Encryption.decrypt_text(self.key, encrypted_string)

        self.assertEqual(test_string, decrypted_string)
