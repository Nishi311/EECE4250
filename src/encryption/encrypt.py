from cryptography.fernet import Fernet


class Encryption(object):

    @staticmethod
    def encrypt_text(key, unencrypted_text):
        fernet_module = Fernet(key)
        encrypted_text = fernet_module.excrypt(b"{0}".format(unencrypted_text))
        return encrypted_text

    @staticmethod
    def decrypt_text(key, encrypted_text):
        fernet_module = Fernet(key)
        decrypted_text = fernet_module.decrypt(b"{0}".format(encrypted_text))
        return decrypted_text

