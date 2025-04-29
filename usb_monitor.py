import win32com.client
import pythoncom

def monitor_usb_connections():
    wmi = win32com.client.GetObject("winmgmts:")
    watcher = wmi.ExecNotificationQuery(
        "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_USBHub'"
    )
    while True:
        pythoncom.PumpWaitingMessages()
        usb = watcher.NextEvent()
        print("USB Connected:", usb.TargetInstance.DeviceID)

