import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QTextEdit, QPushButton, QLabel, QHBoxLayout,
    QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor
from usb_scanner import get_usb_devices
from usb_monitor import start_usb_monitoring
from file_monitor import start_file_monitoring
from report_generator import generate_pdf
from database import USBForensicDB
from alert_system import AlertSystem

class LogEmitter(QObject):
    log_signal = pyqtSignal(str)
    alert_signal = pyqtSignal(str, str)  # (title, message)

class USBForensicGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Forensic Tool")
        self.setGeometry(200, 100, 900, 600)
        self.db = USBForensicDB()
        self.emitter = LogEmitter()
        self.monitoring_active = False
        self.file_monitoring_active = False
        
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.setStyleSheet("""
            background-color: #1a1a2e;
            color: cyan;
            font-family: Consolas;
        """)
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🕵️‍♂️ USB Forensic Tool")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 2px solid cyan; }
            QTabBar::tab { background: #16213e; color: cyan; padding: 10px; }
            QTabBar::tab:selected { background: #0f3460; font-weight: bold; }
        """)

        self.setup_history_tab()
        self.setup_live_tab()
        self.setup_transfer_tab()

        layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("background: #1e1e2d; color: #a0a0c0;")
        layout.addWidget(self.status_bar)
        
        self.setLayout(layout)

    def setup_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.history_output = QTextEdit()
        self.history_output.setReadOnly(True)
        self.history_output.setStyleSheet("""
            font-size: 14px;
            background-color: #0f0f1a;
            color: white;
        """)

        btn_layout = QHBoxLayout()
        
        scan_btn = QPushButton("🔍 Scan USB History")
        report_btn = QPushButton("📄 Generate PDF Report")
        
        for btn in (scan_btn, report_btn):
            btn.setStyleSheet("""
                background-color: #0f3460;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
                border-radius: 4px;
            """)
            btn.setCursor(Qt.PointingHandCursor)

        scan_btn.clicked.connect(self.scan_usb_history)
        report_btn.clicked.connect(self.generate_report)

        btn_layout.addWidget(scan_btn)
        btn_layout.addWidget(report_btn)
        layout.addLayout(btn_layout)
        layout.addWidget(self.history_output)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "USB History")

    def setup_live_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.live_output = QTextEdit()
        self.live_output.setReadOnly(True)
        self.live_output.setStyleSheet("""
            font-size: 14px;
            background-color: #0f0f1a;
            color: white;
        """)

        self.monitor_btn = QPushButton("🔌 Start Live Monitoring")
        self.monitor_btn.setCheckable(True)
        self.monitor_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:checked {
                background-color: #c0392b;
            }
        """)
        self.monitor_btn.clicked.connect(self.toggle_monitoring)

        layout.addWidget(self.monitor_btn)
        layout.addWidget(self.live_output)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Live Logging")

    def setup_transfer_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.transfer_output = QTextEdit()
        self.transfer_output.setReadOnly(True)
        self.transfer_output.setStyleSheet("""
            font-size: 14px;
            background-color: #0f0f1a;
            color: white;
        """)

        self.file_monitor_btn = QPushButton("📂 Start File Monitoring")
        self.file_monitor_btn.setCheckable(True)
        self.file_monitor_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:checked {
                background-color: #c0392b;
            }
        """)
        self.file_monitor_btn.clicked.connect(self.toggle_file_monitoring)

        layout.addWidget(self.file_monitor_btn)
        layout.addWidget(self.transfer_output)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "File Transfers")

    def connect_signals(self):
        self.emitter.log_signal.connect(self.handle_log)
        self.emitter.alert_signal.connect(self.show_alert)

    def handle_log(self, message):
        if "USB" in message:  # Live monitoring messages
            self.live_output.append(message)
        elif any(x in message for x in ["CREATED", "MODIFIED", "DELETED", "MOVED"]):  # File events
            self.transfer_output.append(message)
        else:  # History messages
            self.history_output.append(message)
        
        self.status_bar.showMessage(message[:100] + "..." if len(message) > 100 else message)

    def show_alert(self, title, message):
        QMessageBox.warning(self, title, message)

    def scan_usb_history(self):
        devices = get_usb_devices()
        self.history_output.clear()
        for device in devices:
            self.history_output.append(f"""
Device: {device.get('FriendlyName', 'Unknown')}
├─ Serial: {device.get('Serial', 'Unknown')}
├─ Manufacturer: {device.get('Manufacturer', 'Unknown')}
└─ Last Connected: {device.get('LastConnectedTime', 'Unknown')}
""")

    def generate_report(self):
        devices = get_usb_devices()
        if devices:
            generate_pdf(devices)
            self.history_output.append("\n[✓] PDF report generated: usb_report.pdf")
        else:
            self.history_output.append("\n[!] No USB devices found to generate report")

    def toggle_monitoring(self):
        if self.monitor_btn.isChecked():
            self.monitoring_active = True
            self.monitor_btn.setText("🛑 Stop Monitoring")
            threading.Thread(
                target=start_usb_monitoring,
                args=(lambda msg: self.emitter.log_signal.emit(msg),),
                daemon=True
            ).start()
        else:
            self.monitoring_active = False
            self.monitor_btn.setText("🔌 Start Monitoring")

    def toggle_file_monitoring(self):
        if self.file_monitor_btn.isChecked():
            self.file_monitoring_active = True
            self.file_monitor_btn.setText("🛑 Stop Monitoring")
            threading.Thread(
                target=start_file_monitoring,
                args=(lambda msg: self.emitter.log_signal.emit(msg),),
                daemon=True
            ).start()
        else:
            self.file_monitoring_active = False
            self.file_monitor_btn.setText("📂 Start Monitoring")

def launch_gui():
    app = QApplication(sys.argv)
    window = USBForensicGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()