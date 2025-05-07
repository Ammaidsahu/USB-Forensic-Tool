# gui.py

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout,
    QListWidget, QTextEdit, QFileDialog, QMainWindow, QTableWidget,
    QTableWidgetItem
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from usb_history import get_usb_history
from usb_monitor import get_connected_usb_devices, get_file_transfers
from hash_utils import compute_hashes_for_usb
from report_generator import generate_usb_history_report, generate_hash_report
import os

class ForensicMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Forensic Tool")
        self.setGeometry(100, 100, 1000, 700)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Load all interfaces
        self.home_screen()
        self.usb_history_screen()
        self.live_monitor_screen()
        self.hash_calc_screen()

        # Show home
        self.stack.setCurrentIndex(0)

    def home_screen(self):
        home_widget = QWidget()
        layout = QVBoxLayout()

        icon_label = QLabel()
        icon_pixmap = QPixmap("assets/usb_icon.png").scaled(100, 100)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel("USB Forensic Toolkit")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)

        btn1 = QPushButton("Scan USB History")
        btn2 = QPushButton("USB Live Monitoring")
        btn3 = QPushButton("Hash Calculator")

        for btn in [btn1, btn2, btn3]:
            btn.setFont(QFont("Arial", 14, QFont.Bold))
            btn.setIcon(QIcon("assets/icon.png"))
            btn.setMinimumHeight(50)

        btn1.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn2.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn3.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        layout.addWidget(icon_label)
        layout.addWidget(welcome_label)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        layout.setAlignment(Qt.AlignTop)
        home_widget.setLayout(layout)
        self.stack.addWidget(home_widget)

    def usb_history_screen(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        self.update_usb_history()

        report_btn = QPushButton("Generate USB History Report")
        report_btn.setIcon(QIcon("assets/report_icon.png"))
        report_btn.clicked.connect(generate_usb_history_report)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout.addWidget(QLabel("Previously Connected USBs:"))
        layout.addWidget(self.history_list)
        layout.addWidget(report_btn)
        layout.addWidget(back_btn)

        page.setLayout(layout)
        self.stack.addWidget(page)

    def update_usb_history(self):
        data = get_usb_history()
        display = "\n\n".join(data)
        self.history_list.setText(display)

    def live_monitor_screen(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.live_list = QTextEdit()
        self.live_list.setReadOnly(True)
        self.update_live_monitor()

        refresh_btn = QPushButton("Refresh USB Devices")
        refresh_btn.clicked.connect(self.update_live_monitor)

        file_transfer_btn = QPushButton("File Transfer Activity")
        file_transfer_btn.clicked.connect(self.open_file_transfer_view)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout.addWidget(QLabel("Connected USB Devices:"))
        layout.addWidget(self.live_list)
        layout.addWidget(refresh_btn)
        layout.addWidget(file_transfer_btn)
        layout.addWidget(back_btn)

        page.setLayout(layout)
        self.stack.addWidget(page)

    def update_live_monitor(self):
        data = get_connected_usb_devices()
        self.live_list.setText("\n\n".join(data))

    def open_file_transfer_view(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.transfer_logs = QTextEdit()
        self.transfer_logs.setReadOnly(True)
        self.update_transfer_logs()

        refresh_btn = QPushButton("Refresh File Transfers")
        refresh_btn.clicked.connect(self.update_transfer_logs)

        back_btn = QPushButton("Back to Monitor")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        layout.addWidget(QLabel("Live File Transfer Logs:"))
        layout.addWidget(self.transfer_logs)
        layout.addWidget(refresh_btn)
        layout.addWidget(back_btn)

        page.setLayout(layout)
        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)

    def update_transfer_logs(self):
        logs = get_file_transfers()
        self.transfer_logs.setText("\n\n".join(logs))

    def hash_calc_screen(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.hash_output = QTextEdit()
        self.hash_output.setReadOnly(True)

        scan_btn = QPushButton("Scan and Calculate Hashes")
        scan_btn.clicked.connect(self.calculate_hashes)

        report_btn = QPushButton("Generate Hash Report")
        report_btn.setIcon(QIcon("assets/report_icon.png"))
        report_btn.clicked.connect(generate_hash_report)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout.addWidget(QLabel("USB Hash Calculator:"))
        layout.addWidget(self.hash_output)
        layout.addWidget(scan_btn)
        layout.addWidget(report_btn)
        layout.addWidget(back_btn)

        page.setLayout(layout)
        self.stack.addWidget(page)

    def calculate_hashes(self):
        output = compute_hashes_for_usb()
        self.hash_output.setText(output)
