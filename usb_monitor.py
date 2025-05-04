import time
import win32file
import winreg
from database import USBForensicDB
from alert_system import AlertSystem

active_usb_map = {}
db = USBForensicDB()
alert_system = AlertSystem()  # Initialize with Gmail config

def start_usb_monitoring(log_callback):
    while True:
        try:
            current_drives = get_removable_drives()
            
            # Check for new drives
            for drive in current_drives:
                if drive not in active_usb_map:
                    serial = get_device_serial(drive[0])
                    active_usb_map[drive] = serial
                    log_msg = f"[+] USB inserted: {drive} (Serial: {serial})"
                    log_callback(log_msg)
                    db.log_device(serial, "Unknown")
                    alert_system.check_new_device(serial)

            # Check removed drives
            for drive in list(active_usb_map.keys()):
                if drive not in current_drives:
                    log_callback(f"[-] USB removed: {drive}")
                    del active_usb_map[drive]

            time.sleep(1)
        except Exception as e:
            log_callback(f"[USB Monitor Error] {str(e)}")
            time.sleep(5)

def get_removable_drives():
    drives = []
    try:
        drive_bits = win32file.GetLogicalDrives()
        for i in range(26):
            if drive_bits & (1 << i):
                drive_letter = f"{chr(65 + i)}:"
                if win32file.GetDriveType(f"{drive_letter}\\") == win32file.DRIVE_REMOVABLE:
                    drives.append(drive_letter)
    except Exception as e:
        print(f"Drive detection error: {e}")
    return drives

def get_device_serial(drive_letter):
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, r"SYSTEM\MountedDevices")
        value = winreg.QueryValueEx(key, f"\\DosDevices\\{drive_letter}:")[0]
        return value.hex()[-20:]  # Extract last 20 chars as pseudo-serial
    except:
        return "UNKNOWN"