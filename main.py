# main.py

from PyQt5.QtWidgets import QApplication
from gui import ForensicMainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ForensicMainWindow()
    window.show()
    sys.exit(app.exec_())
