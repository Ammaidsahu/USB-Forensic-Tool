# usb_monitor.py

import win32com.client
import pythoncom
import threading

def start_usb_monitor(callback):
    def monitor():
        pythoncom.CoInitialize()
        wmi = win32com.client.GetObject("winmgmts:")
        watcher = wmi.ExecNotificationQuery(
            "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_USBHub'"
        )
        while True:
            usb = watcher.NextEvent()
            device_id = usb.TargetInstance.DeviceID
            callback(f"[+] USB Connected: {device_id}")

    t = threading.Thread(target=monitor, daemon=True)
    t.start()
