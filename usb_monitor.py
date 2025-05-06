import psutil
import hashlib
import time
import platform
import subprocess
import os
import threading

class USBMonitor:
    def __init__(self, callback=None):
        self.callback = callback
        self.running = False
        self.previous_devices = {}

    def list_usb_devices(self):
        devices = {}
        partitions = psutil.disk_partitions()
        for p in partitions:
            if 'removable' in p.opts or ('/media' in p.mountpoint or '/run/media' in p.mountpoint):
                usage = psutil.disk_usage(p.mountpoint)
                capacity = f"{round(usage.total / (1024**3), 2)} GB"
                hash_md5, hash_sha256 = self.compute_hashes(p.mountpoint)
                serial, manufacturer = self.get_usb_info(p.device)
                devices[p.device] = {
                    'device': p.device,
                    'mountpoint': p.mountpoint,
                    'capacity': capacity,
                    'md5': hash_md5,
                    'sha256': hash_sha256,
                    'serial': serial,
                    'manufacturer': manufacturer
                }
        return devices

    def get_usb_info(self, device):
        if platform.system() == "Windows":
            try:
                cmd = f"wmic diskdrive where InterfaceType='USB' get SerialNumber, Manufacturer /format:list"
                output = subprocess.check_output(cmd, shell=True).decode()
                serial = ""
                manufacturer = ""
                for line in output.splitlines():
                    if "SerialNumber" in line:
                        serial = line.split("=")[1].strip()
                    if "Manufacturer" in line:
                        manufacturer = line.split("=")[1].strip()
                return serial, manufacturer
            except Exception as e:
                print(f"Error: {e}")
                return "", ""
        return "", ""

    def compute_hashes(self, path):
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        try:
            for root, dirs, files in os.walk(path):
                for f in files:
                    full_path = os.path.join(root, f)
                    with open(full_path, 'rb') as file:
                        while chunk := file.read(4096):
                            md5.update(chunk)
                            sha256.update(chunk)
        except:
            return "Error", "Error"
        return md5.hexdigest(), sha256.hexdigest()

    def start(self):
        self.running = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def monitor_loop(self):
        while self.running:
            devices = self.list_usb_devices()
            if devices != self.previous_devices:
                self.previous_devices = devices
                if self.callback:
                    for device, info in devices.items():
                        self.callback("connected", info)  # Trigger callback for new device
            time.sleep(3)

