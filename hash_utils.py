# hash_utils.py

import os
import hashlib

def compute_hashes_for_usb():
    import wmi
    c = wmi.WMI()
    output = []

    for disk in c.Win32_LogicalDisk():
        if disk.DriveType == 2:  # Removable
            path = disk.DeviceID + "\\"
            output.append(f"Scanning {path}")
            for root, _, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'rb') as f:
                            data = f.read()
                            md5 = hashlib.md5(data).hexdigest()
                            sha256 = hashlib.sha256(data).hexdigest()
                        output.append(f"{file}\nMD5: {md5}\nSHA256: {sha256}\n")
                    except:
                        continue
    return "\n".join(output)
