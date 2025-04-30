# file_monitor.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class USBEventHandler(FileSystemEventHandler):
    def __init__(self, log_callback):
        self.log_callback = log_callback

    def on_created(self, event):
        event_type = "Folder" if event.is_directory else "File"
        self.log_callback(f"[+] Created {event_type}: {event.src_path} at {time.ctime()}")

    def on_deleted(self, event):
        event_type = "Folder" if event.is_directory else "File"
        self.log_callback(f"[-] Deleted {event_type}: {event.src_path} at {time.ctime()}")

    def on_modified(self, event):
        event_type = "Folder" if event.is_directory else "File"
        self.log_callback(f"[~] Modified {event_type}: {event.src_path} at {time.ctime()}")

    def on_moved(self, event):
        self.log_callback(f"[→] Moved from {event.src_path} to {event.dest_path} at {time.ctime()}")

def monitor_usb_drive(drive_letter, log_callback):
    path = f"{drive_letter.upper()}:\\"
    if not os.path.exists(path):
        log_callback(f"[!] Drive {path} does not exist.")
        return

    event_handler = USBEventHandler(log_callback)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    log_callback(f"[*] Monitoring file operations in {path}...\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
