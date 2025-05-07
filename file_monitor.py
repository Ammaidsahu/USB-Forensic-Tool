# file_monitor.py

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileTransferHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            log_transfer("Created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            log_transfer("Modified", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            log_transfer("Deleted", event.src_path)

def log_transfer(action, path):
    with open("database/file_transfers.log", "a") as log:
        log.write(f"[{time.ctime()}] {action}: {path}\n")

def monitor_usb_drive(drive_letter):
    observer = Observer()
    handler = FileTransferHandler()
    observer.schedule(handler, drive_letter + ":\\", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
