import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
from database import USBForensicDB
from file_analyzer import FileAnalyzer
from usb_monitor import active_usb_map
import hashlib

db = USBForensicDB()
analyzer = FileAnalyzer()

class USBFileEventHandler(PatternMatchingEventHandler):
    def __init__(self, log_callback, drive_letter):
        super().__init__(patterns=["*"], ignore_directories=False)
        self.log_callback = log_callback
        self.drive_letter = drive_letter
        self.last_event = None

    def on_created(self, event):
        if not event.is_directory:
            self.process_event("CREATED", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.process_event("DELETED", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            # Skip modification events that are part of creation/move operations
            if self.last_event not in ['CREATED', 'MOVED']:
                self.process_event("MODIFIED", event.src_path)
            self.last_event = None

    def on_moved(self, event):
        if not event.is_directory:
            self.process_event("MOVED", event.src_path, event.dest_path)
            self.last_event = 'MOVED'

    def on_closed(self, event):
        if not event.is_directory and self.last_event == 'CREATED':
            self.process_event("CREATED_COMPLETE", event.src_path)
        self.last_event = None

    def process_event(self, event_type, src_path, dest_path=None):
        try:
            device_serial = active_usb_map.get(f"{self.drive_letter}:", "UNKNOWN")
            device_id = db.log_device(device_serial, "Unknown")
            
            log_msg = f"[{event_type}] "
            
            if event_type == "MOVED":
                log_msg += f"{src_path} → {dest_path}"
                size = os.path.getsize(dest_path) / (1024 * 1024) if os.path.exists(dest_path) else 0
                file_hash = analyzer.get_file_hash(dest_path) if os.path.exists(dest_path) else "N/A"
                file_type = analyzer.get_file_type(dest_path) if os.path.exists(dest_path) else "N/A"
                file_path = dest_path
            else:
                log_msg += src_path
                size = os.path.getsize(src_path) / (1024 * 1024) if os.path.exists(src_path) else 0
                file_hash = analyzer.get_file_hash(src_path) if os.path.exists(src_path) else "N/A"
                file_type = analyzer.get_file_type(src_path) if os.path.exists(src_path) else "N/A"
                file_path = src_path

            if event_type not in ["DELETED"]:
                log_msg += f"\n  Size: {size:.2f}MB | Type: {file_type}"
                if file_hash != "N/A":
                    log_msg += f"\n  Hash: {file_hash[:12]}..."

            # Log to database
            if device_id and event_type not in ["CREATED"]:  # Wait for CREATED_COMPLETE
                db.log_file_event(
                    device_id=device_id,
                    event_type=event_type,
                    file_path=file_path,
                    file_size=size,
                    file_hash=file_hash
                )

            # Special handling for copy operations
            if event_type == "CREATED" and os.path.exists(src_path):
                # Check if this is likely a copy operation
                if self._is_copy_operation(src_path):
                    log_msg = f"[COPIED] {src_path}\n" + log_msg.split('\n', 1)[1]
                    event_type = "COPIED"

            self.log_callback(log_msg)
            
            if event_type == "CREATED":
                self.last_event = 'CREATED'

        except Exception as e:
            self.log_callback(f"[ERROR] {str(e)}")

    def _is_copy_operation(self, filepath):
        """Heuristic to detect copy operations"""
        try:
            # Check if file was recently created and matches size of another file
            file_size = os.path.getsize(filepath)
            for root, _, files in os.walk(os.path.dirname(filepath)):
                for f in files:
                    if f != os.path.basename(filepath):
                        other_path = os.path.join(root, f)
                        if os.path.getsize(other_path) == file_size:
                            return True
            return False
        except:
            return False

def start_file_monitoring(log_callback):
    observers = {}
    
    while True:
        try:
            current_drives = [d[0] for d in active_usb_map.keys()]
            
            # Start new observers
            for drive in current_drives:
                if drive not in observers:
                    path = f"{drive}:\\"
                    if os.path.exists(path):
                        try:
                            event_handler = USBFileEventHandler(log_callback, drive)
                            observer = Observer()
                            observer.schedule(event_handler, path, recursive=True)
                            observer.start()
                            observers[drive] = observer
                            log_callback(f"[*] Started monitoring files on {path}")
                        except Exception as e:
                            log_callback(f"[!] Failed to monitor {path}: {str(e)}")

            # Clean up removed drives
            for drive in list(observers.keys()):
                if drive not in current_drives:
                    observers[drive].stop()
                    observers[drive].join()
                    del observers[drive]
                    log_callback(f"[*] Stopped monitoring {drive}:")

            time.sleep(2)
        except Exception as e:
            log_callback(f"[MONITOR ERROR] {str(e)}")
            time.sleep(5)