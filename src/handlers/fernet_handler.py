from __future__ import annotations

from cryptography.fernet import Fernet


class FernetKeyHandler:
    def __call__(self):
        return self.generateFernetKey()

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
