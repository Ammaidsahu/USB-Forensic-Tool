from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import threading

class FileTransferHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            self.callback("Created", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.callback("Deleted", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.callback("Modified", event.src_path)

class FileTransferMonitor:
    def __init__(self, path, callback):
        self.path = path
        self.callback = callback
        self.observer = Observer()

    def start(self):
        event_handler = FileTransferHandler(self.callback)
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def stop(self):
        self.observer.stop()
