# usb_monitor.py

import wmi
import os
import time

def get_connected_usb_devices():
    result = []
    c = wmi.WMI()
    for disk in c.Win32_DiskDrive():
        if "USB" in disk.InterfaceType:
            try:
                size_gb = int(disk.Size) / (1024**3)
            except:
                size_gb = "Unknown"
            result.append(f"Device: {disk.Caption}\nSerial: {disk.SerialNumber or 'Unknown'}\nSize: {size_gb:.2f} GB")
    return result

def get_file_transfers():
    log_file = "database/file_transfers.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            return f.readlines()
    return ["No transfers logged."]
