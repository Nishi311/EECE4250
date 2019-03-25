from cryptography.fernet import Fernet


class Encryption(object):

    @staticmethod
    def encrypt_text(key, unencrypted_text):
        fernet_module = Fernet(key)
        encrypted_text = fernet_module.encrypt(str.encode(unencrypted_text))
        return encrypted_text

    @staticmethod
    def decrypt_text(key, encrypted_text):
        fernet_module = Fernet(key)
        decrypted_text = fernet_module.decrypt(encrypted_text).decode("utf-8")
        return decrypted_text

