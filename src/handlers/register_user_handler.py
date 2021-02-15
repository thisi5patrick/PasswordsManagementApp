from __future__ import annotations

from .fernet_handler import FernetKeyHandler
from os.path import dirname, join

scriptdir = dirname(__file__)


class RegisterUserHandler:
    def __init__(self, login: str, password: str):
        self._input_login = login
        self._input_password = password
        self.Fernet_handler = FernetKeyHandler(self._input_login, self._input_password)
        self._key = self.Fernet_handler.getFernetKey()

    def userExists(self) -> bool:
        """
        Check if user exists in file with users.
        """
        try:
            with open(join(scriptdir, '..', 'data/users/users.txt'), 'r') as file:
                for line in file:
                    if not line.strip():
                        continue
                    line = line.split(',')
                    _file_login = self._key.decrypt(bytes(line[0], encoding='utf-8'))
                    _input_login = bytes(self._input_login, encoding='utf-8')
                    if _file_login == _input_login:
                        return True
            return False

        except FileNotFoundError:
            return False

    def addUserToFile(self) -> None:
        """
        Add users credentials to file.
        """
        with open(join(scriptdir, '..', 'data/users/users.txt'), 'a') as file:
            _login_with_Fernet = self.Fernet_handler.getLoginHash()
            _password_with_Fernet = self.Fernet_handler.getPasswordHash()
            file.write(f'{_login_with_Fernet},{_password_with_Fernet}\n')
