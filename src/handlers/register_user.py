from __future__ import annotations

from cryptography.fernet import Fernet


class RegisterUser:
    def __init__(self, login: str, password: str):
        self._input_login = login
        self._input_password = password
        self._key = open('src/data/fernet_key.txt', 'rb').readline()
        self._Fernet = Fernet(self._key)

    def checkUserExistence(self) -> bool:
        """
        Check if user exists in file with users.
        """
        try:
            with open('src/data/users/users.txt', 'r') as file:
                for line in file:
                    if not line.strip():
                        continue
                    line = line.split(',')
                    _file_login = self._Fernet.decrypt(bytes(line[0], encoding='utf-8'))
                    _input_login = bytes(self._input_login, encoding='utf-8')
                    if _file_login == _input_login:
                        return True
            return False

        except FileNotFoundError:
            return False

    def getLoginHash(self) -> bytes:
        """
        Method to return user's hashed username.
        :return:
        """

        return self._Fernet.encrypt(bytes(self._input_login, encoding='utf-8')).decode('utf-8')

    def getPasswordHash(self) -> bytes:
        """
        Method to return user's hashed password
        :return:
        """

        return self._Fernet.encrypt(bytes(self._input_password, encoding='utf-8')).decode('utf-8')

    def addUserToFile(self) -> None:
        """
        Add users credentials to file.
        """
        with open('src/data/users/users.txt', 'a') as file:
            _login_with_Fernet = self.getLoginHash()
            _password_with_Fernet = self.getPasswordHash()
            file.write(f'{_login_with_Fernet},{_password_with_Fernet}\n')
