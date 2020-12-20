from __future__ import annotations


class RegisterUser:
    def __init__(self, login: str, password: str):
        self._login = login
        self._password = password

    def checkUserExistence(self) -> bool:
        """
        Check if user exists in file with users.
        """
        user_exists = False
        try:
            with open('src/data/users.txt', 'r') as file:
                for line in file:
                    if line == f'{self._login},{self._password}':
                        user_exists = True
            return user_exists

        except FileNotFoundError:
            return user_exists

    def addUserToFile(self) -> None:
        """
        Add users credentials to file.
        """
        with open('src/data/users.txt', 'a') as file:
            file.write(f'{self._login},{self._password}\n')
