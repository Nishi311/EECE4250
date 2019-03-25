import unittest
from src.encryption.encrypt import Encryption


class ControllerTester(unittest.TestCase):
    def setup(self):
        self.key = "This is a testing key"

    def test_encryption(self):
        test_string = "Hello World"
        encrypted_string = Encryption.encrypt_text(self.key, test_string)

        self.assertNotEqual(test_string, encrypted_string)

    def test_encryption(self):
        test_string = "Hello World"
        encrypted_string = Encryption.encrypt_text(self.key, test_string)
        decrypted_string = Encryption.decrypt_text(self.key, encrypted_string)

        self.assertEqual(test_string, decrypted_string)
