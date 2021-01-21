from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QLabel, QFormLayout, QPushButton, QWidget, QFrame, QSplitter, QHBoxLayout
from ..handlers.logged_in_user import LoggedInUser


class LogedUserWindow(QWidget):
    def __init__(self, parent):
        super(LogedUserWindow, self).__init__(parent)
        self.parent = parent

    def initUI(self, _login):
        """
        Method to init the UI of user
        """
        self.user_handler = LoggedInUser(_login)
        self.login_label = QLabel('&Enter your login: ')
        self.layout = QFormLayout()
        self.layout.addWidget(self.login_label)
        self.setLayout(self.layout)
