from __future__ import annotations

from cryptography.fernet import Fernet


class FernetKeyHandler:
    def __init__(self, _login = None, _password = None):
        self._key = open('src/data/fernet_key.txt', 'rb').readline()
        self._Fernet = Fernet(self._key)
        self._login = _login
        self._password = _password

    def getFernetKey(self) -> bytes:
        """
        Return Fernet object to decrypt and encrypt texts
        :return:
        """

        return self._Fernet

    @staticmethod
    def generateKey() -> bytes:
        """
        Generate Fernet Key.
        """
        return Fernet.generate_key()

    @staticmethod
    def writeKeyToFile(file, key: str):
        """
        Write Fernet Key to file
        """
        file.write(key)

    def generateFernetKey(self) -> bytes:
        """
        Check if Fernet Key is generated.
        If it is, then read it from file, else generate key.
        """
        try:
            with open('src/data/fernet_key.txt', 'br+') as f:
                FernetKey = f.readline()
                if FernetKey == b'':
                    key = self.generateKey()
                    self.writeKeyToFile(f, key)
                return FernetKey

        except FileNotFoundError:
            key = self.generateKey()
            with open('src/data/fernet_key.txt', 'wb') as f:
                self.writeKeyToFile(f, key)

        return key

    def getPasswordHash(self) -> bytes:
        """
        Method to return user's hashed password
        :return: hashed password
        """

        return self._Fernet.encrypt(bytes(self._password, encoding='utf-8')).decode('utf-8')

    def getLoginHash(self) -> bytes:
        """
        Method to return user's hashed username.
        :return: hashed username
        """

        return self._Fernet.encrypt(bytes(self._login, encoding='utf-8')).decode('utf-8')
