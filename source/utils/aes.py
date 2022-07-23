from aes_cipher import DataEncrypter, DataDecrypter
from base64 import encodebytes, decodebytes


class Aes:
    @staticmethod
    def encrypt(raw: str, password: str) -> str:
        de = DataEncrypter()
        de.Encrypt(raw, [password])

        return encodebytes(de.GetEncryptedData()).decode('UTF-8')

    @staticmethod
    def decrypt(encoded: str, password: str) -> str:
        dd = DataDecrypter()
        dd.Decrypt(decodebytes(encoded.encode()), [password])

        return dd.GetDecryptedData().decode('UTF-8')
