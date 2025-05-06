import sqlite3
import os
from PyQt5.QtWidgets import QMessageBox
from config import DATABASE, Config  # Make sure DATABASE is defined in the config

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_path = DATABASE['path']
        
        # Create database directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Database Error", f"Failed to connect to database: {str(e)}")

    def create_tables(self):
        """Create necessary tables in the database."""
        try:
            # USB History Table
            self.cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS usb_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_name TEXT,
                    serial_number TEXT UNIQUE,
                    manufacturer TEXT,
                    hash_md5 TEXT,
                    hash_sha256 TEXT,
                    storage_capacity TEXT,
                    first_connected TEXT,
                    last_connected TEXT,
                    vendor_id TEXT,
                    product_id TEXT
                )
            ''')

            # Live USB Events Table
            self.cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS live_usb_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    device_name TEXT,
                    serial_number TEXT,
                    timestamp TEXT,
                    details TEXT
                )
            ''')

            # File Transfer Events Table
            self.cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS file_transfer_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    file_path TEXT,
                    usb_serial TEXT,
                    timestamp TEXT,
                    file_hash_md5 TEXT,
                    file_hash_sha256 TEXT,
                    file_size TEXT,
                    is_suspicious INTEGER DEFAULT 0
                )
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Database Error", f"Failed to create tables: {str(e)}")

    def insert_usb_history(self, device_data):
        """Insert or replace a USB device's history record."""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO usb_history 
                (device_name, serial_number, manufacturer, hash_md5, hash_sha256, 
                 storage_capacity, first_connected, last_connected, vendor_id, product_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                device_data['device_name'],
                device_data['serial_number'],
                device_data['manufacturer'],
                device_data['hash_md5'],
                device_data['hash_sha256'],
                device_data['storage_capacity'],
                device_data['first_connected'],
                device_data['last_connected'],
                device_data['vendor_id'],
                device_data['product_id']
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting USB history: {str(e)}")
            return False

    def get_usb_history(self):
        """Retrieve USB device history."""
        try:
            self.cursor.execute('SELECT * FROM usb_history ORDER BY last_connected DESC')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching USB history: {str(e)}")
            return []

    def insert_live_event(self, event_type, device_name, serial_number, timestamp, details):
        """Insert live event data."""
        try:
            self.cursor.execute('''
                INSERT INTO live_usb_events 
                (event_type, device_name, serial_number, timestamp, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (event_type, device_name, serial_number, timestamp, details))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting live event: {str(e)}")
            return False

    def get_live_events(self):
        """Retrieve all live USB events."""
        try:
            self.cursor.execute('SELECT * FROM live_usb_events ORDER BY timestamp DESC')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching live events: {str(e)}")
            return []

    def insert_file_transfer_event(self, event_data):
        """Insert file transfer event data."""
        try:
            self.cursor.execute('''
                INSERT INTO file_transfer_events 
                (event_type, file_path, usb_serial, timestamp, 
                 file_hash_md5, file_hash_sha256, file_size, is_suspicious)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_data['event_type'],
                event_data['file_path'],
                event_data['usb_serial'],
                event_data['timestamp'],
                event_data['file_hash_md5'],
                event_data['file_hash_sha256'],
                event_data['file_size'],
                event_data['is_suspicious']
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting file transfer event: {str(e)}")
            return False

    def get_file_transfer_events(self, usb_serial=None):
        """Retrieve file transfer events for a specific USB serial or all events."""
        try:
            if usb_serial:
                self.cursor.execute('''
                    SELECT * FROM file_transfer_events 
                    WHERE usb_serial = ? 
                    ORDER BY timestamp DESC
                ''', (usb_serial,))
            else:
                self.cursor.execute('SELECT * FROM file_transfer_events ORDER BY timestamp DESC')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching file transfer events: {str(e)}")
            return []

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()


# Singleton database instance
db_manager = DatabaseManager()

if __name__ == "__main__":
    # Example of inserting a USB device history
    device_data = {
        "device_name": "USB Device 1",
        "serial_number": "12345ABC",
        "manufacturer": "Generic Manufacturer",
        "hash_md5": "abc123md5",
        "hash_sha256": "sha256hash123",
        "storage_capacity": "64GB",
        "first_connected": "2025-05-06 10:00:00",
        "last_connected": "2025-05-06 10:05:00",
        "vendor_id": "VID_1234",
        "product_id": "PID_5678"
    }
    db_manager.insert_usb_history(device_data)

    # Example of inserting a file transfer event
    event_data = {
        "event_type": "Created",
        "file_path": "/path/to/file.txt",
        "usb_serial": "12345ABC",
        "timestamp": "2025-05-06 10:10:00",
        "file_hash_md5": "hashmd5file123",
        "file_hash_sha256": "sha256filehash123",
        "file_size": "2MB",
        "is_suspicious": 0
    }
    db_manager.insert_file_transfer_event(event_data)

    # Retrieve all USB history
    usb_history = db_manager.get_usb_history()
    print(usb_history)

    # Retrieve all file transfer events
    file_transfers = db_manager.get_file_transfer_events()
    print(file_transfers)

    db_manager.close()
