import time
import threading
from usb_monitor import USBMonitor
from file_monitor import USBFileMonitor
from config import Config

class BackgroundService:
    def __init__(self, usb_callback, file_callback):
        self.usb_callback = usb_callback
        self.file_callback = file_callback
        self.usb_monitor = None
        self.file_monitor = None

    def start(self):
        """Start the background service to monitor USB and file system events."""
        self.usb_monitor = USBMonitor(self.usb_callback)
        self.usb_monitor.start()

        # Periodically check for USB device activity
        threading.Thread(target=self._monitor_usb, daemon=True).start()

    def _monitor_usb(self):
        """Monitor USB events and pass them to the callback."""
        while True:
            # We can add some other background logic here if needed.
            time.sleep(3)

    def start_file_monitoring(self, path):
        """Start monitoring file events on a given USB drive path."""
        self.file_monitor = USBFileMonitor(path, self.file_callback)
        self.file_monitor.start()

    def stop(self):
        """Stop all background monitoring services."""
        if self.usb_monitor:
            self.usb_monitor.stop()
        if self.file_monitor:
            self.file_monitor.stop()

    def restart(self):
        """Restart the service."""
        self.stop()
        time.sleep(2)  # Add delay before restarting
        self.start()

if __name__ == "__main__":
    # Example callbacks
    def usb_callback(devices):
        print("USB devices detected:", devices)

    def file_callback(event_type, src_path):
        print(f"File {event_type}: {src_path}")

    service = BackgroundService(usb_callback, file_callback)
    service.start()
