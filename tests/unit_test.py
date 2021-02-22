import unittest
from os.path import exists, join, dirname
import shutil
import re

from src.handlers import FoldersHandler, RegisterUserHandler, FernetKeyHandler, LoggedInUserHandler

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

    def testCheckFernetKey(self):
        self.assertIsInstance(self.fernet_handler._key, bytes)

    def testCheckUserHash(self):
        self.assertRegex(self.fernet_handler.getLoginHash(), r'^gAAAAABg.{90}==$')


class RegisterUserTest(unittest.TestCase):
    def testCheckFakeUserExistence(self):
        user_handler = RegisterUserHandler('test1', 'test2')
        self.assertFalse(user_handler.userExists() is False)

    def testChackTrueUserExistence(self):
        user_handler = RegisterUserHandler('test1', 'test2')
        user_handler.addUserToFile()
        self.assertTrue(user_handler.userExists() is True)


class LoggedUserTest(unittest.TestCase):
    def setUp(self) -> None:
        login_password = 'test1'
        fernet_handler = FernetKeyHandler(login_password, login_password)
        login = fernet_handler.getLoginHash()
        user_handler = RegisterUserHandler(login_password, login_password)
        user_handler.addUserToFile()
        user_handler.createFileForPasswords(login)
        self.user_handler = LoggedInUserHandler(login_password)

    def testFileExistence(self):
        self.assertIsNot(self.user_handler.getFile(), None)

    def testNoneExistentUser(self):
        wrong_user_handler = LoggedInUserHandler('NonExistentUser')
        self.assertIs(wrong_user_handler.file, None)

    def testHashString(self):
        self.assertIsInstance(self.user_handler.hashStrings('value1'), list)
        self.assertIsInstance(self.user_handler.hashStrings('value1', 'value2'), list)
        self.assertIsInstance(self.user_handler.hashStrings('value1')[0], bytes)

    def testUserHash(self):
        self.assertRegex(self.user_handler.getUserHash(), r'^gAAAAABg.{90}==$')

    def testWriteAccountToFile(self):
        with self.user_handler.getFile() as file:
            lines_before = file.read().split('\n')
        self.user_handler.writeAccountToFile(['value4', 'value5', 'value6'])

        with self.user_handler.getFile() as file:
            lines_after = file.read().split('\n')
        self.assertNotEqual(lines_before, lines_after)

    def testToBytes(self):
        self.assertIsInstance(self.user_handler.toBytes('test'), bytes)
        self.assertIsInstance(self.user_handler.toBytes(['test', 'test2'])[0], bytes)

    def testToString(self):
        self.assertIsInstance(self.user_handler.toString(b'test'), str)
        self.assertIsInstance(self.user_handler.toString([b'test', b'test2'])[0], str)

    # TODO add test
    def testDeleteAccountFromFile(self):
        ...

    def doCleanups(self) -> None:
        shutil.rmtree(join(scriptdir, '..', 'src', 'data', 'passwords'), ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
