# gui.py

import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QTextEdit,
    QPushButton, QLabel, QHBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from usb_scanner import parse_usb_history
from usb_monitor import start_usb_monitor
from file_monitor import monitor_usb_drive
from report_generator import generate_pdf


class USBForensicGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Forensic Tool")
        self.setGeometry(200, 100, 950, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #00d9ff;
                font-family: Consolas;
                font-size: 14px;
            }
            QLabel#welcomeLabel {
                font-size: 28px;
                font-weight: bold;
                color: #00e0ff;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #00e0ff;
                color: #0a0a0a;
                font-weight: bold;
                padding: 14px;
                border-radius: 10px;
                font-size: 15px;
                min-width: 240px;
            }
            QPushButton:hover {
                background-color: #009db3;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #101020;
                color: #00ffcc;
                border: 2px solid #00e0ff;
                font-family: Consolas;
                font-size: 13px;
            }
            QTabWidget::pane {
                border: 2px solid #00e0ff;
            }
            QTabBar::tab {
                background: #292949;
                padding: 10px;
                color: #00e0ff;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #00e0ff;
                color: #0a0a0a;
            }
        """)

        self.layout = QVBoxLayout()

        # Welcome Note
        welcome = QLabel("🕵️‍♂️ Welcome to USB Forensic Tool")
        welcome.setObjectName("welcomeLabel")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setFont(QFont("Consolas", 24, QFont.Bold))
        self.layout.addWidget(welcome)

        # Tabs
        self.tabs = QTabWidget()
        self.history_tab = QWidget()
        self.live_tab = QWidget()
        self.transfer_tab = QWidget()

        self.init_history_tab()
        self.init_live_tab()
        self.init_transfer_tab()

        self.tabs.addTab(self.history_tab, "USB History")
        self.tabs.addTab(self.live_tab, "Live Logging")
        self.tabs.addTab(self.transfer_tab, "File Transfers")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # 1. USB History Tab
    def init_history_tab(self):
        layout = QVBoxLayout()
        self.history_output = QTextEdit()
        self.history_output.setReadOnly(True)

        # Centered Buttons
        button_layout = QHBoxLayout()
        scan_btn = QPushButton("🔍 Scan USB History")
        report_btn = QPushButton("📄 Export PDF Report")
        scan_btn.clicked.connect(self.show_usb_history)
        report_btn.clicked.connect(self.generate_report)

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(scan_btn)
        button_layout.addWidget(report_btn)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(button_layout)
        layout.addWidget(self.history_output)
        self.history_tab.setLayout(layout)

    def show_usb_history(self):
        devices = parse_usb_history()
        self.history_output.clear()
        for d in devices:
            self.history_output.append(
                f"Device: {d['Device']} | Serial: {d['Serial']} | Name: {d['FriendlyName']}"
            )

    def generate_report(self):
        data = parse_usb_history()
        generate_pdf(data)
        self.history_output.append("\n[✓] PDF Report Generated: usb_report.pdf")

    # 2. Live Logging Tab
    def init_live_tab(self):
        layout = QVBoxLayout()
        self.live_output = QTextEdit()
        self.live_output.setReadOnly(True)

        button_layout = QHBoxLayout()
        start_btn = QPushButton("⚡ Start Live Monitoring")
        start_btn.clicked.connect(lambda: threading.Thread(
            target=start_usb_monitor,
            args=(self.append_live_log,),
            daemon=True
        ).start())

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(start_btn)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(button_layout)
        layout.addWidget(self.live_output)
        self.live_tab.setLayout(layout)

    def append_live_log(self, msg):
        self.live_output.append(msg)

    # 3. File Transfer Monitoring Tab
    def init_transfer_tab(self):
        layout = QVBoxLayout()
        self.transfer_output = QTextEdit()
        self.transfer_output.setReadOnly(True)

        button_layout = QHBoxLayout()
        start_btn = QPushButton("📁 Monitor File Transfers (Drive E:)")
        start_btn.clicked.connect(lambda: threading.Thread(
            target=monitor_usb_drive,
            args=("E", self.append_transfer_log),
            daemon=True
        ).start())

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(start_btn)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(button_layout)
        layout.addWidget(self.transfer_output)
        self.transfer_tab.setLayout(layout)

    def append_transfer_log(self, log):
        self.transfer_output.append(log)


def launch_gui():
    app = QApplication(sys.argv)
    window = USBForensicGUI()
    window.show()
    sys.exit(app.exec_())
