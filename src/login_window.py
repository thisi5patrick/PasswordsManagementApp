from __future__ import annotations

from PyQt5.QtWidgets import QLineEdit, QLabel, QFormLayout, QPushButton, QWidget

from .fernet_handler import FernetKeyHandler


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

        layout = QFormLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def checkCredentials(self):
        """
        Function to check entered credentials
        """
        # TODO create class to check credentials
        print(self.login_input.text())

    def registerUser(self):
        """
        Method to create a new account for user
        """
        self.parent.stacked_widget.setCurrentIndex(self.parent.stacked_widget.currentIndex() + 1)
