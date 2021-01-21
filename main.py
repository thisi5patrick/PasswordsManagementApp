from __future__ import annotations

from PyQt5.QtWidgets import QApplication
import sys
from src.windows import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wizard = MainWindow()
    wizard.show()
    sys.exit(app.exec_())
