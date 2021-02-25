from __future__ import annotations

import re

from PyQt5.QtWidgets import QLabel, QFormLayout, QPushButton, QWidget, QLineEdit, QListWidget, \
    QListWidgetItem, QGridLayout, QAbstractItemView
from src.handlers import FernetKeyHandler, LoggedInUserHandler


class LayerWidget(QWidget):
    def __init__(self, layer, parent):
        super(LayerWidget, self).__init__()
        self.user_handler = parent
        self.website_label = QLabel()
        self.login_label = QLabel()
        self.password_label = QLabel()
        self.login_text = None
        self.password_text = None
        self.asterisk_password = None

        layout = QGridLayout()
        layout.addWidget(QLabel('Website'), 0, 0)
        layout.addWidget(QLabel('Login'), 1, 0)
        layout.addWidget(QLabel('Password'), 2, 0)
        layout.addWidget(self.website_label, 0, 1, 1, 3)
        layout.addWidget(self.login_label, 1, 1, 1, 3)
        layout.addWidget(self.password_label, 2, 1, 1, 3)

        self._layer = None
        self.layer = layer

        delete_account_button = QPushButton('Delete')
        delete_account_button.clicked.connect(lambda state, arg=self.login_text: self.deleteAccount(arg))
        delete_account_button.setStyleSheet('''
            QPushButton { font-size: 12px;}
        ''')

        self.show_password_button = QPushButton('Show')
        self.show_password_button.clicked.connect(lambda state: self.showPassword())
        self.show_password_button.setStyleSheet('''
            QPushButton { font-size: 12px;}
        ''')
        layout.addWidget(self.show_password_button, 2, 5)
        layout.addWidget(delete_account_button, 0, 5, 2, 1)
        self.setLayout(layout)

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value
        self.asterisk_password = re.sub('.', '*', value.get('password'))
        self.password_label.setText(self.asterisk_password)
        self.website_label.setText(value.get('website'))
        self.password_text = value.get('password')
        self.login_label.setText(value.get('login'))
        self.login_text = value.get('login')

    def deleteAccount(self, login: str):
        self.user_handler.deleteAccountFromFile(login)

    def showPassword(self):
        """
        Change password from '*' to string
        """
        self.password_label.setText(self.password_text)


class LogedUserWindow(QWidget):
    def __init__(self, parent):
        super(LogedUserWindow, self).__init__(parent)
        self.parent = parent
        self.setStyleSheet('''
            QPushButton { padding: 10px 0px; }
        ''')
        self.fernet_handler = FernetKeyHandler()

    def initUI(self, _login: str):
        """
        Init the UI of user
        """
        self.user_handler = LoggedInUserHandler(_login)
        _accounts = self.user_handler.getSavedAccounts()
        self.welcome_message = QLabel(f'Welcome back {_login}')
        self.welcome_message.setStyleSheet('''
            QLabel { margin-bottom: 15px; font-size: 12px}
        ''')

        self.layout = QFormLayout()
        self.website_label = QLabel('&Enter website address:')
        self.website_input = QLineEdit()
        self.website_label.setBuddy(self.website_input)

        self.login_label = QLabel('&Enter login:')
        self.login_input = QLineEdit()
        self.login_label.setBuddy(self.login_input)

        self.password_label = QLabel('&Enter password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_label.setBuddy(self.password_input)

        self.add_account_button = QPushButton('Add account')
        self.add_account_button.clicked.connect(self.addAccountToFile)

        self.info_label = QLabel()

        listWidget = QListWidget()
        listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        for account in _accounts.values():
            widget = LayerWidget(layer=account, parent=self.user_handler)
            item = QListWidgetItem()
            listWidget.insertItem(listWidget.count(), item)
            listWidget.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

        self.layout.addWidget(self.welcome_message)
        self.layout.addWidget(self.website_label)
        self.layout.addWidget(self.website_input)
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.add_account_button)
        self.layout.addWidget(listWidget)
        self.setLayout(self.layout)

    @staticmethod
    def toStrings(list_of_bytes: list) -> list:
        """
        Method to convert list of bytes to list of string
        :param list_of_bytes: list of bytes
        :return: converted list bytes to string
        """
        list_of_string = []
        for item in list_of_bytes:
            list_of_string.append(item.decode('utf-8'))
        return list_of_string

    def addAccountToFile(self):
        """

        """
        if not (self.password_input.text() and self.website_input.text() and self.login_input.text()):
            self.info_label.setText('All inputs must be filled.')
            self.info_label.setStyleSheet('color: red; font-size: 12px;')
            return

        self.user_handler.writeAccountToFile([self.website_input.text(),
                                              self.login_input.text(),
                                              self.password_input.text()])
        self.info_label.setText('Account succesfully saved.')
        self.info_label.setStyleSheet('font-size: 12px;')
