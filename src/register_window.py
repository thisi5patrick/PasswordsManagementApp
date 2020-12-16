from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QPushButton
from PyQt5.QtGui import QValidator


class RegisterWindow(QWidget):
    def __init__(self, parent):
        super(RegisterWindow, self).__init__(parent)
        self.parent = parent

        self.wrong_password = QLabel()

        self.new_login_label = QLabel('&Enter your new login: ')
        self.new_login_input = QLineEdit()
        self.new_login_label.setBuddy(self.new_login_input)

        self.new_password_label = QLabel('&Enter your password: ')
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_label.setBuddy(self.new_password_input)

        self.new_password_repeat_label = QLabel('&Enter your password: ')
        self.new_password_repeat_input = QLineEdit()
        self.new_password_repeat_input.setEchoMode(QLineEdit.Password)
        self.new_password_repeat_label.setBuddy(self.new_password_repeat_input)

        buttonNext = QPushButton('Create new account')

        buttonNext.clicked.connect(self.createNewAccount)

        self.layout = QFormLayout()
        self.layout.addWidget(self.new_login_label)
        self.layout.addWidget(self.new_login_input)
        self.layout.addWidget(self.new_password_label)
        self.layout.addWidget(self.new_password_input)
        self.layout.addWidget(self.new_password_repeat_label)
        self.layout.addWidget(self.new_password_repeat_input)
        self.layout.addWidget(self.wrong_password)
        self.layout.addWidget(buttonNext)
        self.setLayout(self.layout)

    def validatePassword(self) -> bool:
        """
        Validate if passwords are the same
        :return: True if passwords match each other
        """
        if self.new_password_input.text() == self.new_password_repeat_input.text():
            return True
        else:
            return False

    def createNewAccount(self) -> None:
        """
        Create account based on credentials provided
        """
        if self.validatePassword():
            self.parent.stacked_widget.setCurrentIndex(self.parent.stacked_widget.currentIndex() - 1)
        else:
            self.wrong_password.setText('Passwords does not match!')
            self.wrong_password.setStyleSheet('color: red; font-size: 12px;')
