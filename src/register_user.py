from __future__ import annotations


class RegisterUser:
    def __init__(self, login: str, password: str):
        self._login = login
        self._password = password

    # TODO check if user exists
    # TODO check if file 'users.txt' exists
    def addUserToFile(self):
        f = open('src/data/users.txt', 'a')
        f.write(f'{self._login},{self._password}')
        f.close()
