# gui.py
import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QTextEdit, QPushButton
)
from usb_scanner import parse_usb_history
from usb_monitor import start_usb_monitor
from file_monitor import monitor_usb_drive
from report_generator import generate_pdf


class USBForensicGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Forensic Tool")
        self.setGeometry(200, 100, 800, 600)
        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()

        # Tabs
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

        scan_btn = QPushButton("Scan USB History")
        report_btn = QPushButton("Export PDF Report")

        scan_btn.clicked.connect(self.show_usb_history)
        report_btn.clicked.connect(self.generate_report)

        layout.addWidget(scan_btn)
        layout.addWidget(report_btn)
        layout.addWidget(self.history_output)

        self.history_tab.setLayout(layout)

    def show_usb_history(self):
        devices = parse_usb_history()
        self.history_output.clear()
        for d in devices:
            self.history_output.append(f"Device: {d['Device']} | Serial: {d['Serial']} | Name: {d['FriendlyName']}")

    def generate_report(self):
        data = parse_usb_history()
        generate_pdf(data)
        self.history_output.append("\n[✓] PDF Report Generated: usb_report.pdf")

    # 2. Live Logging Tab
    def init_live_tab(self):
        layout = QVBoxLayout()
        self.live_output = QTextEdit()
        self.live_output.setReadOnly(True)

        start_btn = QPushButton("Start Live Monitoring")
        start_btn.clicked.connect(lambda: threading.Thread(target=start_usb_monitor, args=(self.append_live_log,), daemon=True).start())

        layout.addWidget(start_btn)
        layout.addWidget(self.live_output)
        self.live_tab.setLayout(layout)

    def append_live_log(self, msg):
        self.live_output.append(msg)

    # 3. File Transfer Monitoring Tab
    def init_transfer_tab(self):
        layout = QVBoxLayout()
        self.transfer_output = QTextEdit()
        self.transfer_output.setReadOnly(True)

        start_btn = QPushButton("Start File Monitoring (Drive E:)")
        start_btn.clicked.connect(lambda: threading.Thread(target=monitor_usb_drive, args=("E", self.append_transfer_log), daemon=True).start())

        layout.addWidget(start_btn)
        layout.addWidget(self.transfer_output)
        self.transfer_tab.setLayout(layout)

    def append_transfer_log(self, log):
        self.transfer_output.append(log)


def launch_gui():
    app = QApplication(sys.argv)
    window = USBForensicGUI()
    window.show()
    sys.exit(app.exec_())
