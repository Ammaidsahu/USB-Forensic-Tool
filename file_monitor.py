from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class USBHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"File created: {event.src_path}")

def monitor_usb_drive(drive_letter):
    observer = Observer()
    handler = USBHandler()
    path = f"{drive_letter}:/"
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()