from aes_cipher import DataEncrypter, DataDecrypter


class Aes:
    @staticmethod
    def encrypt(raw: str, password: str) -> bytes:
        de = DataEncrypter()
        de.Encrypt(raw, [password])

        return de.GetEncryptedData()

    @staticmethod
    def decrypt(encoded: bytes, password: str) -> str:
        dd = DataDecrypter()
        dd.Decrypt(encoded, [password])

        return dd.GetDecryptedData().decode('UTF-8')
