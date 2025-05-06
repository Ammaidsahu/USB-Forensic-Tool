# usb_scanner.py
import winreg
import hashlib
import os
from datetime import datetime

def get_usb_history():
    history = []
    try:
        reg_path = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                device_key_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, device_key_name) as device_key:
                    for j in range(winreg.QueryInfoKey(device_key)[0]):
                        instance_id = winreg.EnumKey(device_key, j)
                        full_path = f"{reg_path}\\{device_key_name}\\{instance_id}"
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, full_path) as instance_key:
                            try:
                                manufacturer, _ = winreg.QueryValueEx(instance_key, "Mfg")
                            except:
                                manufacturer = "Unknown"
                            try:
                                last_connected = winreg.QueryInfoKey(instance_key)[2]
                                last_connected = datetime.fromtimestamp(last_connected / 1e7 - 11644473600)
                            except:
                                last_connected = "N/A"
                            try:
                                serial_number = instance_id
                            except:
                                serial_number = "N/A"

                        device = {
                            "Device Name": device_key_name,
                            "Serial Number": serial_number,
                            "Manufacturer": manufacturer,
                            "Last Connected": str(last_connected),
                            "Capacity": get_device_capacity(serial_number),
                            "Hash MD5": generate_hash(serial_number, "md5"),
                            "Hash SHA256": generate_hash(serial_number, "sha256"),
                        }
                        history.append(device)
    except Exception as e:
        print("Error reading registry:", e)
    return history

def get_device_capacity(serial_number):
    # Dummy value as capacity can't be found via registry directly
    return "Unknown (Runtime check needed)"

def generate_hash(input_str, algorithm="md5"):
    h = hashlib.new(algorithm)
    h.update(input_str.encode("utf-8"))
    return h.hexdigest()
