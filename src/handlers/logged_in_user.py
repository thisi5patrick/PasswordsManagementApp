from .fernet_handler import FernetKeyHandler
from collections import defaultdict
import os


class LoggedInUser:
    def __init__(self, _login):
        super(LoggedInUser, self).__init__()
        self._login = _login
        self.Fernet_handler = FernetKeyHandler(self._login)
        self.file = self.getFile()

    @staticmethod
    def toString(str_of_bytes: bytes) -> str:
        """
        Method to convert bytes to string
        :param str_of_bytes: string of bytes
        :return: converted bytes to string
        """

        string = str_of_bytes.decode('utf-8')
        return string

    @staticmethod
    def toBytes(list_of_strings: list) -> list:
        """

        :param list_of_strings:
        :return:
        """
        list_of_bytes = []
        for item in list_of_strings:
            list_of_bytes.append(bytes(item, encoding='utf-8'))

        return list_of_bytes

    def getSavedAccounts(self) -> dict:
        """
        Return a list of all saved accounts.
        :return: list of saved accounts
        """
        accounts = defaultdict(list)
        for idx, line in enumerate(self.getFile()):
            line = line[:-1].split(',')
            line = self.toBytes(line)
            website = self.toString(self.Fernet_handler.Fernet.decrypt(line[0]))
            login = self.toString(self.Fernet_handler.Fernet.decrypt(line[1]))
            password = self.toString(self.Fernet_handler.Fernet.decrypt(line[2]))

            accounts[idx].append([website, login, password])

        return accounts

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
            file.write(f'{list_of_items[0]},{list_of_items[1]},{list_of_items[2]}\n')
