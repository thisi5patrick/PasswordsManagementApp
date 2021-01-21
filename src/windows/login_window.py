from __future__ import annotations

from PyQt5.QtWidgets import QLineEdit, QLabel, QFormLayout, QPushButton, QWidget

from src.handlers import FernetKeyHandler
from src.windows.logged_user_window import LogedUserWindow


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        fernet_key_handler = FernetKeyHandler()
        self._key = fernet_key_handler()
        self.parent = parent
        self.setStyleSheet('''
            QLabel { font-size: 12px; margin-top: 40px }
            QPushButton { padding: 10px 0px; margin-top: 10px; }
        ''')

        self.login_label = QLabel('&Enter your login: ')
        self.login_input = QLineEdit()
        self.login_label.setBuddy(self.login_input)

        self.password_label = QLabel('&Enter your password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_label.setBuddy(self.password_input)

        self.login_button = QPushButton('Log In')
        self.login_button.clicked.connect(self.checkCredentials)

        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.registerUser)

        self.layout = QFormLayout()
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def checkCredentials(self):
        """
        Function to check entered credentials
        """
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        LogedUserWindow(self)

    def registerUser(self):
        """
        Method to create a new account for user
        """
        self.parent.stacked_widget.setCurrentIndex(self.parent.stacked_widget.currentIndex() + 1)
