from .fernet_handler import FernetKeyHandler


class LoggedInUser:
    def __init__(self, _login):
        super(LoggedInUser, self).__init__()
        self._login = _login
        self.Fernet_handler = FernetKeyHandler(self._login)

    def getUserHash(self):
        """
        Return user's login hash
        :return: login hash
        """

        return self.Fernet_handler.getLoginHash()
