import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileTransferHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    
    def on_modified(self, event):
        self.callback("modified", event.src_path)
    
    def on_created(self, event):
        self.callback("created", event.src_path)
    
    def on_deleted(self, event):
        self.callback("deleted", event.src_path)

class FileTransferMonitor:
    def __init__(self, path, callback):
        self.path = path
        self.callback = callback
        self.observer = Observer()
    
    def start(self):
        event_handler = FileTransferHandler(self.callback)
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
