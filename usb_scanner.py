from Registry import Registry

def parse_usb_history():
    reg = Registry.Registry("C:\\Windows\\System32\\config\\SYSTEM")
    key = reg.open("CurrentControlSet\\Enum\\USBSTOR")
    devices = []
    for subkey in key.subkeys():
        for instance in subkey.subkeys():
            device = {
                "Device": subkey.name(),
                "Serial": instance.name(),
                "LastWrite": instance.timestamp(),
                "FriendlyName": instance.value("FriendlyName").value() if instance.value("FriendlyName") else "N/A"
            }
            devices.append(device)
    return devices