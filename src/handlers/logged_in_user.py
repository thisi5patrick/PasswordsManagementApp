from __future__ import annotations
from typing import Union

from .fernet_handler import FernetKeyHandler
import os


class LoggedInUser:
    def __init__(self, _login):
        super(LoggedInUser, self).__init__()
        self._login = _login
        self.Fernet_handler = FernetKeyHandler(self._login)
        self.file = self.getFile()

    @staticmethod
    def toString(items_to_convert: Union[bytes, list]) -> Union[str, list]:
        """
        Method to convert bytes or list to string
        :param items_to_convert: bytes or list of bytes
        :return: converted bytes or list to string
        """
        if isinstance(items_to_convert, bytes):
            return_value = items_to_convert.decode('utf-8')
        else:
            return_value = []
            items = list(*items_to_convert)
            for item in items:
                return_value.append(item.decode('utf-8'))
        return return_value

    @staticmethod
    def toBytes(items_to_convert: Union[list, str]) -> Union[str, list]:
        """
        Convert str or list to bytes
        :param items_to_convert: list or str
        :return: converted list or str to bytes
        """
        if isinstance(items_to_convert, str):
            return_value = bytes(items_to_convert, encoding='utf-8')
        else:
            return_value = []
            for item in items_to_convert:
                return_value.append(bytes(item, encoding='utf-8'))
        return return_value

    def getSavedAccounts(self) -> dict:
        """
        Return a list of all saved accounts.
        :return: list of saved accounts
        """
        accounts = dict()
        for idx, line in enumerate(self.getFile()):
            line = line[:-1].split(',')
            line = self.toBytes(line)
            website = self.toString(self.Fernet_handler.Fernet.decrypt(line[0]))
            login = self.toString(self.Fernet_handler.Fernet.decrypt(line[1]))
            password = self.toString(self.Fernet_handler.Fernet.decrypt(line[2]))

            accounts[idx] = {
                'website': website,
                'login': login,
                'password': password
            }

        return accounts

    def deleteAccountFromFile(self, login: str):
        """
        Delete account data from file
        :param login: login to delete
        """
        with self.getFile() as file:
            text = file.read()
            file.seek(0)
            for line in text.split('\n'):
                if not line:
                    break
                decrypted_login = self.toString(self.Fernet_handler.Fernet.decrypt(self.toBytes(line.split(',')[1])))
                if decrypted_login != login:
                    file.write(line + '\n')

            file.truncate()

    def getFile(self):
        """
        Get file object
        :return: file object
        """
        for file in os.listdir('src/data/passwords/'):
            bytes_file = bytes(file, encoding='utf-8')
            if self.Fernet_handler.Fernet.decrypt(bytes_file) == bytes(self._login, encoding='utf-8'):
                return open(f'src/data/passwords/{file}', 'r+')

    def getUserHash(self):
        """
        Return user's login hash
        :return: login hash
        """

        return self.Fernet_handler.getLoginHash()

    def hashStrings(self, *values: str) -> list:
        """
        Use Fernet key to encrypt items
        :param values:  strings to encrypt
        :return: list of encrtypted items
        """
        hashed_items = []
        for item in values:
            hashed_items.append(self.Fernet_handler.Fernet.encrypt(bytes(item, encoding='utf-8')))

        return hashed_items

    def writeAccountToFile(self, list_of_items: list):
        """
        Write account data to file
        :param list_of_items: list of items to write to file
        """
        with self.getFile() as file:
            file.read()
            file.write(f'{list_of_items[0]},{list_of_items[1]},{list_of_items[2]}\n')
