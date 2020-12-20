from __future__ import annotations

from cryptography.fernet import Fernet


class RegisterUser:
    def __init__(self, login: str, password: str):
        self._login = login
        self._password = password
        self._key = open('src/data/fernet_key.txt', 'rb').readline()
        self._Fernet = Fernet(self._key)

    def checkUserExistence(self) -> bool:
        """
        Check if user exists in file with users.
        """
        try:
            with open('src/data/users/users.txt', 'r') as file:
                for line in file:
                    line = line.split(',')
                    _login = bytes(line[0], encoding='utf-8')
                    _login = self._Fernet.decrypt(_login)
                    _password = self._Fernet.decrypt(bytes(line[1], encoding='utf-8'))
                    self._login = bytes(self._login, encoding='utf-8')
                    self._password = bytes(self._password, encoding='utf-8')
                    if f'{_login},{_password}' == f'{self._login},{self._password}':
                        return True
            return False

        except FileNotFoundError:
            return False

    def addUserToFile(self) -> None:
        """
        Add users credentials to file.
        """
        with open('src/data/users/users.txt', 'a') as file:
            _login_with_Fernet = self._Fernet.encrypt(bytes(self._login, encoding='utf8'))
            _password_with_Fernet = self._Fernet.encrypt(bytes(self._password, encoding='utf8'))
            file.write(f'{_login_with_Fernet.decode("utf-8")},{_password_with_Fernet.decode("utf-8")}\n')
