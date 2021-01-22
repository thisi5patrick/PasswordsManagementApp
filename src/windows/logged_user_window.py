from __future__ import annotations

from PyQt5.QtWidgets import QLabel, QFormLayout, QPushButton, QWidget, QLineEdit, QVBoxLayout, QListWidget, \
    QListWidgetItem, QHBoxLayout, QLayout
from src.handlers import FernetKeyHandler, LoggedInUser


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
        Method to init the UI of user
        """
        self.user_handler = LoggedInUser(_login)
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
        # listWidget.setSizeConstraint(QLayout.SetFixedSize)
        main_layout = QHBoxLayout()
        main_layout.addWidget(listWidget)

        # TODO display registered accounts - not working
        for account in _accounts.values():
            website = QLabel(account[0][0])
            login = QLabel(account[0][1])
            password = QLabel(account[0][2])

            widget = QWidget()
            widget.addWidget(website)
            widget.addWidget(login)
            widget.addWidget(password)

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
        list_of_hashed_items = self.user_handler.hashStrings(self.website_input.text(),
                                                             self.login_input.text(),
                                                             self.password_input.text())

        list_of_hashed_items = self.toStrings(list_of_hashed_items)
        self.user_handler.writeAccountToFile(list_of_hashed_items)
        self.info_label.setText('Account succesfully saved.')
        self.info_label.setStyleSheet('font-size: 12px;')
