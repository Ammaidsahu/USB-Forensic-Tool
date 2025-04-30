import os
import winreg

def parse_usb_history():
    devices = []
    try:
        path = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, path)

        for i in range(winreg.QueryInfoKey(key)[0]):
            device_key_name = winreg.EnumKey(key, i)
            device_key = winreg.OpenKey(key, device_key_name)

            for j in range(winreg.QueryInfoKey(device_key)[0]):
                instance_name = winreg.EnumKey(device_key, j)
                instance_key_path = path + "\\" + device_key_name + "\\" + instance_name
                instance_key = winreg.OpenKey(reg, instance_key_path)

                try:
                    friendly_name, _ = winreg.QueryValueEx(instance_key, "FriendlyName")
                except:
                    friendly_name = "N/A"

                devices.append({
                    "Device": device_key_name,
                    "Serial": instance_name,
                    "FriendlyName": friendly_name
                })

    except Exception as e:
        devices.append({"Error": str(e)})

    return devices
