import sqlite3
from datetime import datetime
import threading

class USBForensicDB:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_db()
        return cls._instance
    
    def _init_db(self):
        self.conn = sqlite3.connect('usb_forensics.db', check_same_thread=False)
        self._create_tables()
        
    def _create_tables(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usb_devices (
                    id INTEGER PRIMARY KEY,
                    serial TEXT UNIQUE,
                    manufacturer TEXT,
                    first_seen TEXT,
                    last_seen TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_events (
                    id INTEGER PRIMARY KEY,
                    device_id INTEGER,
                    event_type TEXT,
                    file_path TEXT,
                    file_size REAL,
                    file_hash TEXT,
                    timestamp TEXT,
                    FOREIGN KEY(device_id) REFERENCES usb_devices(id)
                )
            ''')
    
    def log_device(self, serial, manufacturer):
        with self._lock:
            try:
                cursor = self.conn.cursor()
                now = datetime.now().isoformat()
                
                cursor.execute('SELECT id FROM usb_devices WHERE serial=?', (serial,))
                device = cursor.fetchone()
                
                if device:
                    cursor.execute('''
                        UPDATE usb_devices SET last_seen=? WHERE id=?
                    ''', (now, device[0]))
                    device_id = device[0]
                else:
                    cursor.execute('''
                        INSERT INTO usb_devices (serial, manufacturer, first_seen, last_seen)
                        VALUES (?, ?, ?, ?)
                    ''', (serial, manufacturer, now, now))
                    device_id = cursor.lastrowid
                
                self.conn.commit()
                return device_id
            except Exception as e:
                print(f"Database error: {e}")
                return None
    
    def log_file_event(self, device_id, event_type, file_path, file_size, file_hash):
        with self._lock:
            try:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO file_events 
                    (device_id, event_type, file_path, file_size, file_hash, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (device_id, event_type, file_path, file_size, file_hash, datetime.now().isoformat()))
                self.conn.commit()
            except Exception as e:
                print(f"Database error: {e}")

    def get_device_history(self, serial):
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM usb_devices WHERE serial=?', (serial,))
            return cursor.fetchone()

    def get_file_events(self, device_id):
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM file_events WHERE device_id=? ORDER BY timestamp DESC
            ''', (device_id,))
            return cursor.fetchall()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()