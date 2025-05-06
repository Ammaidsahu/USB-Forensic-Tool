import hashlib
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QListWidget, QWidget

class HashCalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hash Calculator")
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout()

        # Create a list widget to display USB device info
        self.device_list = QListWidget()
        self.layout.addWidget(self.device_list)

        # Add a button or other UI components here
        self.load_usb_devices()

        # Set up the layout and container
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_usb_devices(self):
        """Load the list of USB devices and calculate hashes."""
        # Replace with logic to get connected USBs
        usb_devices = ["USB Device 1", "USB Device 2"]  # Simulating devices
        for device in usb_devices:
            md5_hash = hashlib.md5(device.encode()).hexdigest()
            sha256_hash = hashlib.sha256(device.encode()).hexdigest()
            self.device_list.addItem(f"{device} - MD5: {md5_hash} - SHA256: {sha256_hash}")
