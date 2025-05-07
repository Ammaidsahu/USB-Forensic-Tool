# usb_history.py

import winreg


def get_usb_history():
    path = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
    history = []

    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, path)
        for i in range(1024):
            try:
                device_key_name = winreg.EnumKey(key, i)
                device_key = winreg.OpenKey(key, device_key_name)

                for j in range(1024):
                    try:
                        subkey_name = winreg.EnumKey(device_key, j)
                        subkey = winreg.OpenKey(device_key, subkey_name)
                        try:
                            desc, _ = winreg.QueryValueEx(subkey, "FriendlyName")
                        except:
                            desc = "Unknown"
                        try:
                            mfg, _ = winreg.QueryValueEx(subkey, "Manufacturer")



                        except:
                            mfg = "Unknown"
                        try:
                            sn = subkey_name.split("&")[-1]
                        except:
                            sn = "N/A"

                        history.append(f"Device: {desc}\nManufacturer:Sanddisk \nSerial: {sn}")
                    except:
                        break
            except:
                break
        winreg.CloseKey(key)
    except Exception as e:
        history.append(f"Error reading registry: {e}")
    return history
