# usb_monitor.py
import time
import win32file

def start_usb_monitor(log_callback):
    drives = get_removable_drives()
    log_callback("[*] Monitoring started... Insert or remove USB devices.\n")

    while True:
        time.sleep(1)
        new_drives = get_removable_drives()
        inserted = [d for d in new_drives if d not in drives]
        removed = [d for d in drives if d not in new_drives]

        for d in inserted:
            log_callback(f"[+] USB inserted: {d}")
        for d in removed:
            log_callback(f"[-] USB removed: {d}")

        drives = new_drives

def get_removable_drives():
    drives = []
    drive_bits = win32file.GetLogicalDrives()
    for i in range(1, 26):
        mask = 1 << i
        if drive_bits & mask:
            drive_letter = f"{chr(65 + i)}:\\"
            try:
                drive_type = win32file.GetDriveType(drive_letter)
                if drive_type == win32file.DRIVE_REMOVABLE:
                    drives.append(drive_letter)
            except Exception:
                continue
    return drives
