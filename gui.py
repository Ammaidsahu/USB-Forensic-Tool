import sys
import time
import logging
import hashlib
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QTextEdit, QStackedWidget, QSizePolicy, QProgressBar, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import wmi

# Configure logging
logging.basicConfig(filename='usb_forensic_tool.log', level=logging.DEBUG)

class USBFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        logging.info(f'File modified: {event.src_path}')
        print(f'File modified: {event.src_path}')

    def on_created(self, event):
        if event.is_directory:
            return
        logging.info(f'File created: {event.src_path}')
        print(f'File created: {event.src_path}')

    def on_deleted(self, event):
        if event.is_directory:
            return
        logging.info(f'File deleted: {event.src_path}')
        print(f'File deleted: {event.src_path}')

class MonitorThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.running = True

    def run(self):
        event_handler = USBFileHandler()
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()
        while self.running:
            time.sleep(1)
        observer.stop()
        observer.join()

    def stop(self):
        self.running = False

class USBMonitor:
    def __init__(self, callback):
        self.callback = callback

    def start(self):
        # Simulating USB connection and removal detection
        # This would be replaced with actual monitoring code
        self.callback("connected", "D:")
        time.sleep(2)
        self.callback("removed", "D:")

class USBFileMonitor(QThread):
    def __init__(self, path, callback):
        super().__init__()
        self.path = path
        self.callback = callback

    def run(self):
        # Simulate file monitoring (replace with actual file system event monitoring)
        time.sleep(1)
        self.callback("created", "file1.txt")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Forensic Tool")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #0F111A; color: white;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.home_widget = self.create_home_page()
        self.central_widget.addWidget(self.home_widget)

    def create_home_page(self):
        home = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel()
        icon = QPixmap("assets/usb_icon.png").scaled(120, 120, Qt.KeepAspectRatio)
        icon_label.setPixmap(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        welcome_label = QLabel("\U0001F50D Welcome to the USB Forensic Tool")
        welcome_label.setFont(QFont("Arial", 20, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        layout.addSpacing(30)

        button_font = QFont("Arial", 14, QFont.Bold)
        button_style = """
            QPushButton {
                background-color: #1F2235;
                color: white;
                padding: 15px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #343650;
            }
        """

        buttons = [
            ("assets/history.png", "Scan USB History", self.show_usb_history),
            ("assets/live.png", "USB Live Monitoring", self.show_live_monitor),
            ("assets/hash.png", "Hash Calculator", self.show_hash_calculator),
            ("assets/transfer.png", "File Transfer Monitor", self.show_file_transfer_monitor),
        ]

        for icon_path, text, callback in buttons:
            btn = QPushButton(f"  {text}")
            btn.setFont(button_font)
            btn.setStyleSheet(button_style)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QPixmap(icon_path).size())
            btn.setMinimumHeight(60)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
            layout.addSpacing(10)

        home.setLayout(layout)
        return home

    def show_usb_history(self):
        history_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("\U0001F9FE USB History Log")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout()

        usb_data = self.get_usb_history()
        if not usb_data:
            label = QLabel("No historical USB data found.")
            label.setFont(QFont("Arial", 12))
            content_layout.addWidget(label)
        else:
            for device in usb_data:
                dev_box = QTextEdit()
                dev_box.setFont(QFont("Consolas", 10))
                dev_box.setReadOnly(True)
                dev_box.setStyleSheet("background-color: #1E1E2F; color: white; border: 1px solid #555;")
                dev_text = "\n".join([f"Device Name      : {device['Device Name']}",
                                      f"Serial Number    : {device['Serial Number']}",
                                      f"Manufacturer     : {device['Manufacturer']}",
                                      f"Last Connected   : {device['Last Connected']}",
                                      f"Capacity         : {device['Capacity']}",
                                      f"MD5 Hash         : {device['Hash MD5']}",
                                      f"SHA256 Hash      : {device['Hash SHA256']}"])
                dev_box.setText(dev_text)
                content_layout.addWidget(dev_box)
                content_layout.addSpacing(10)

        pdf_btn = QPushButton("\U0001F4C4 Generate PDF Report")
        pdf_btn.setFont(QFont("Arial", 12, QFont.Bold))
        pdf_btn.setStyleSheet("padding: 10px; background-color: #3C3F58;")
        pdf_btn.clicked.connect(lambda: self.generate_pdf_report(usb_data))
        content_layout.addWidget(pdf_btn)

        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        history_widget.setLayout(layout)
        self.central_widget.addWidget(history_widget)
        self.central_widget.setCurrentWidget(history_widget)

    def get_usb_history(self):
        # Replace with actual USB history fetching logic
        return [{"Device Name": "USB Drive 1", "Serial Number": "123456", "Manufacturer": "Manufacturer A", "Last Connected": "2025-05-01", "Capacity": "64GB", "Hash MD5": "abcd1234", "Hash SHA256": "abcd1234567890"}]

    def generate_pdf_report(self, usb_data):
        filename = "usb_history_report.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, "USB Forensic Report")
        c.drawString(100, 730, "USB history log generated.")
        c.save()

        logging.info(f"PDF report generated: {filename}")
        QMessageBox.information(self, "Report Generated", f"PDF report saved as {filename}.")

    def show_live_monitor(self):
        self.live_monitor_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("\U0001F50C Live USB Monitoring")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.usb_activity_log = QTextEdit()
        self.usb_activity_log.setReadOnly(True)
        self.usb_activity_log.setStyleSheet("background-color: #1E1E2F; color: white;")
        layout.addWidget(self.usb_activity_log)

        self.live_monitor_widget.setLayout(layout)
        self.central_widget.addWidget(self.live_monitor_widget)
        self.central_widget.setCurrentWidget(self.live_monitor_widget)

        self.start_usb_monitoring()

    def start_usb_monitoring(self):
        def usb_callback(event_type, drive):
            if event_type == "connected":
                self.usb_activity_log.append(f"\u2705 USB Connected: {drive}")
            elif event_type == "removed":
                self.usb_activity_log.append(f"\u274C USB Removed: {drive}")

        self.usb_monitor = USBMonitor(usb_callback)
        self.usb_monitor.start()

    def show_hash_calculator(self):
        print("Show Hash Calculator - To be implemented")

    def show_file_transfer_monitor(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("\U0001F4C2 File Transfer Monitor Interface")
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
