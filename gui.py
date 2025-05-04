import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QTextEdit, QPushButton, QLabel, QHBoxLayout,
    QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor
from usb_scanner import USBForensicScanner
from usb_monitor import start_usb_monitoring
from file_monitor import start_file_monitoring
from report_generator import generate_pdf
from database import USBForensicDB
from alert_system import AlertSystem

class LogEmitter(QObject):
    log_signal = pyqtSignal(str)
    alert_signal = pyqtSignal(str, str)  # (title, message)
    progress_signal = pyqtSignal(int)

class USBForensicGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Forensic Tool")
        self.setGeometry(200, 100, 1000, 700)
        self.scanner = USBForensicScanner()
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
        
        # Main layout
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🕵️‍♂️ USB Forensic Tool")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: cyan;
            margin-bottom: 15px;
        """)
        layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 2px solid cyan; }
            QTabBar::tab {
                background: #16213e;
                color: cyan;
                padding: 10px;
                font-size: 16px;
            }
            QTabBar::tab:selected {
                background: #0f3460;
                font-weight: bold;
            }
        """)

        self.setup_history_tab()
        self.setup_live_tab()
        self.setup_transfer_tab()

        layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            background: #1e1e2d;
            color: #a0a0c0;
            padding: 5px;
            font-size: 12px;
        """)
        layout.addWidget(self.status_bar)
        
        self.setLayout(layout)

    def setup_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.history_output = QTextEdit()
        self.history_output.setReadOnly(True)
        self.history_output.setStyleSheet("""
            font-family: Consolas;
            font-size: 14px;
            background-color: #0f0f1a;
            color: white;
            border: 1px solid #2b7bba;
            border-radius: 4px;
        """)

        btn_layout = QHBoxLayout()
        
        scan_btn = QPushButton("🔍 Scan USB History")
        report_btn = QPushButton("📄 Generate PDF Report")
        clear_btn = QPushButton("🗑️ Clear Log")
        
        for btn in (scan_btn, report_btn, clear_btn):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0f3460;
                    color: white;
                    padding: 8px 15px;
                    font-size: 14px;
                    border-radius: 4px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #3a8cca;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)

        scan_btn.clicked.connect(self.scan_usb_history)
        report_btn.clicked.connect(self.generate_report)
        clear_btn.clicked.connect(self.history_output.clear)

        btn_layout.addWidget(scan_btn)
        btn_layout.addWidget(report_btn)
        btn_layout.addWidget(clear_btn)
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
            font-family: Consolas;
            font-size: 14px;
            background-color: #0f0f1a;
            color: white;
            border: 1px solid #2b7bba;
            border-radius: 4px;
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
                border: none;
            }
            QPushButton:checked {
                background-color: #c0392b;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:checked:hover {
                background-color: #e74c3c;
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
            font-family: Consolas;
            font-size: 14px;
            background-color: #0f0f1a;
            color: white;
            border: 1px solid #2b7bba;
            border-radius: 4px;
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
                border: none;
            }
            QPushButton:checked {
                background-color: #c0392b;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:checked:hover {
                background-color: #e74c3c;
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
        self.emitter.progress_signal.connect(self.update_progress)

    def handle_log(self, message):
        if "USB" in message:  # Live monitoring messages
            self.live_output.append(message)
            self.live_output.ensureCursorVisible()
        elif any(x in message for x in ["CREATED", "MODIFIED", "DELETED", "MOVED"]):  # File events
            self.transfer_output.append(message)
            self.transfer_output.ensureCursorVisible()
        else:  # History messages
            self.history_output.append(message)
        
        self.status_bar.showMessage(message[:100] + "..." if len(message) > 100 else message)

    def show_alert(self, title, message):
        QMessageBox.warning(self, title, message)

    def update_progress(self, value):
        self.status_bar.showMessage(f"Scanning... {value}%")

    def scan_usb_history(self):
        self.history_output.clear()
        self.status_bar.showMessage("Scanning USB history...")
        
        # Run in separate thread to keep GUI responsive
        threading.Thread(
            target=self._perform_scan,
            daemon=True
        ).start()

    def _perform_scan(self):
        devices = self.scanner.get_usb_devices()
        if not devices:
            self.emitter.log_signal.emit("No USB devices found or access denied")
            return
            
        for device in devices:
            log_msg = (
                f"Device: {device['FriendlyName']}\n"
                f"├─ Serial: {device['Serial']}\n"
                f"├─ Manufacturer: {device['Manufacturer']}\n"
                f"├─ Last Connected: {device['LastConnectedTime']}\n"
                f"└─ Detected via: {device.get('DetectionMethod', 'Unknown')}\n"
            )
            self.emitter.log_signal.emit(log_msg)
        
        self.emitter.log_signal.emit(f"\nFound {len(devices)} USB device(s)")
        self.status_bar.showMessage("Scan completed")

    def generate_report(self):
        devices = self.scanner.get_usb_devices()
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
    
    # Set dark theme palette
    palette = app.palette()
    palette.setColor(palette.Window, QColor(30, 30, 45))
    palette.setColor(palette.WindowText, QColor(200, 200, 255))
    palette.setColor(palette.Base, QColor(15, 15, 26))
    palette.setColor(palette.AlternateBase, QColor(40, 40, 60))
    palette.setColor(palette.Text, QColor(200, 200, 255))
    palette.setColor(palette.Button, QColor(50, 50, 70))
    palette.setColor(palette.ButtonText, QColor(200, 200, 255))
    palette.setColor(palette.Highlight, QColor(43, 123, 186))
    palette.setColor(palette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = USBForensicGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()