from __future__ import annotations

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QPushButton
from PyQt5.QtGui import QValidator

from .register_user import RegisterUser


class RegisterWindow(QWidget):
    def __init__(self, parent):
        super(RegisterWindow, self).__init__(parent)
        self._password = None
        self._login = None
        self.parent = parent

        self.info_label = QLabel()

        self.new_login_label = QLabel('&Enter your new login: ')
        self._new_login_input = QLineEdit()
        self.new_login_label.setBuddy(self._new_login_input)

        self.info_about_password = QLabel('&Your password should ')

        self.new_password_label = QLabel('&Enter your password: ')
        self._new_password_input = QLineEdit()
        self._new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_label.setBuddy(self._new_password_input)

        self.new_password_repeat_label = QLabel('&Enter your password: ')
        self._new_password_repeat_input = QLineEdit()
        self._new_password_repeat_input.setEchoMode(QLineEdit.Password)
        self.new_password_repeat_label.setBuddy(self._new_password_repeat_input)

        buttonNext = QPushButton('Create new account')

        buttonNext.clicked.connect(self.createNewAccount)

        self.layout = QFormLayout()
        self.layout.addWidget(self.new_login_label)
        self.layout.addWidget(self._new_login_input)
        self.layout.addWidget(self.new_password_label)
        self.layout.addWidget(self._new_password_input)
        self.layout.addWidget(self.new_password_repeat_label)
        self.layout.addWidget(self._new_password_repeat_input)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(buttonNext)
        self.setLayout(self.layout)

    def validatePassword(self) -> bool:
        """
        Validate if passwords are the same
        :return: True if passwords match each other
        """
        return self._new_password_input.text() == self._new_password_repeat_input.text()

    def createNewAccount(self) -> None:
        """
        Create account based on credentials provided
        """
        self._password = self._new_password_input.text()
        self._login = self._new_login_input.text()
        if self.validatePassword():
            ru = RegisterUser(self._login, self._password)
            if not ru.checkUserExistence():
                ru.addUserToFile()
                self._new_login_input.clear()
                self._new_password_input.clear()
                self._new_password_repeat_input.clear()
                self.parent.stacked_widget.setCurrentIndex(self.parent.stacked_widget.currentIndex() - 1)
            else:
                self.info_label.setText('User already exists')
                self.info_label.setStyleSheet('color: red; font-size: 12px;')
                self._new_password_input.clear()
                self._new_password_repeat_input.clear()
        else:
            self.info_label.setText('Passwords does not match!')
            self.info_label.setStyleSheet('color: red; font-size: 12px;')
