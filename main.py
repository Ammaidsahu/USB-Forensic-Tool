from PyQt5.QtWidgets import QApplication
import sys
from gui import MainWindow  # Import your MainWindow class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("USB Forensic Tool")  # Setting application name
    
    window = MainWindow()
    window.show()  # Show the main window
    
    sys.exit(app.exec_())  # Start the application event loop
