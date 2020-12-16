from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from . import LoginWindow
from . import RegisterWindow


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Password Manager')
        self.setGeometry(500, 200, 400, 500)

        main_layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()

        self.stacked_widget.addWidget(LoginWindow(self))
        self.stacked_widget.addWidget(RegisterWindow(self))

        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
