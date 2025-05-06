import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

# Define dangerous or malicious file extensions
MALICIOUS_EXTENSIONS = ['.exe', '.bat', '.vbs', '.scr']

# Function to check if a file is malicious based on its extension
def is_malicious(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in MALICIOUS_EXTENSIONS

# Custom event handler for file transfers
class USBFileEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback  # callback to pass events to the GUI

    def on_created(self, event):
        """Triggered when a new file is created"""
        if is_malicious(event.src_path):
            self.callback('malicious', event.src_path)
        else:
            self.callback('created', event.src_path)

    def on_deleted(self, event):
        """Triggered when a file is deleted"""
        self.callback('deleted', event.src_path)

    def on_modified(self, event):
        """Triggered when a file is modified"""
        if is_malicious(event.src_path):
            self.callback('malicious', event.src_path)
        else:
            self.callback('modified', event.src_path)

    def on_moved(self, event):
        """Triggered when a file is moved"""
        self.callback('moved', event.src_path, event.dest_path)

# USB File Monitoring Class
class USBFileMonitor:
    def __init__(self, path, callback):
        self.event_handler = USBFileEventHandler(callback)
        self.observer = Observer()
        self.path = path

    def start(self):
        """Start monitoring the file system for changes on the USB device"""
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()

    def stop(self):
        """Stop monitoring the file system"""
        self.observer.stop()
        self.observer.join()

# Function to start monitoring file events on a USB drive
def start_monitoring(directory, callback):
    event_handler = USBFileEventHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            pass  # Keep the observer running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
