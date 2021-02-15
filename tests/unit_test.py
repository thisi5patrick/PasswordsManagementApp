import unittest
from os.path import exists, join, dirname
import shutil
import re

from src.handlers import FoldersHandler, RegisterUserHandler, FernetKeyHandler

scriptdir = dirname(__file__)


class FoldersTest(unittest.TestCase):
    def setUp(self) -> None:
        shutil.rmtree(join(scriptdir, '..', 'src', 'data'), ignore_errors=True)
        folder_handler = FoldersHandler()
        folder_handler.createFolders()

    def testCheckDataFolder(self):
        data_folder = exists(join(scriptdir, '..', 'src', 'data'))
        self.assertIs(data_folder, True)

    def testCheckPasswordsFolder(self):
        passwords_folder = exists(join(scriptdir, '..', 'src', 'data', 'passwords'))
        self.assertIs(passwords_folder, True)

    def testCheckUsersFolder(self):
        users_folder = exists(join(scriptdir, '..', 'src', 'data', 'users'))
        self.assertIs(users_folder, True)


class FernetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fernet_handler = FernetKeyHandler('test', 'test')
        self.fernet_handler.generateFernetKey()

    def testCheckFernetKey(self):
        self.assertIsInstance(self.fernet_handler._key, bytes)

    def testCheckUserHash(self):
        patten = re.compile('^gAAAAABg.{90}==$')
        self.assertNotEqual(patten.match(self.fernet_handler.getLoginHash()), None)


class RegisterUserTest(unittest.TestCase):
    def setUp(self) -> None:
        FernetKeyHandler('test', 'test').generateFernetKey()

    def testCheckFakeUserExistence(self):
        user_handler = RegisterUserHandler('test1', 'test2')
        self.assertFalse(user_handler.userExists() is False)

    def testChackTrueUserExistence(self):
        user_handler = RegisterUserHandler('test1', 'test2')
        user_handler.addUserToFile()
        self.assertTrue(user_handler.userExists() is True)


if __name__ == '__main__':
    unittest.main()
