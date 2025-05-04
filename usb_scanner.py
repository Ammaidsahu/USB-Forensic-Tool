import winreg
import datetime
import struct
import ctypes
import sys
import threading
from typing import List, Dict

class USBForensicScanner:
    def __init__(self):
        self._com_initialized = False

    def is_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def filetime_to_dt(self, filetime: bytes) -> str:
        """Convert Windows FILETIME to readable datetime"""
        try:
            if not filetime or len(filetime) != 8:
                return "Unknown"
            
            timestamp = struct.unpack('<Q', filetime)[0]
            if timestamp == 0:
                return "Unknown"
                
            timestamp = timestamp / 10_000_000 - 11644473600
            return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return "Unknown"

    def _get_usb_devices_wmi(self):
        """WMI-based USB detection with proper COM handling"""
        devices = []
        try:
            import pythoncom
            import wmi
            pythoncom.CoInitialize()
            self._com_initialized = True
            
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive(InterfaceType="USB"):
                try:
                    # Extract serial from PNPDeviceID
                    serial = "Unknown"
                    if disk.PNPDeviceID:
                        parts = disk.PNPDeviceID.split('\\')
                        if len(parts) > 2:
                            serial = parts[2].split('&')[0]
                    
                    # Convert install date
                    last_connected = "Unknown"
                    if disk.InstallDate:
                        try:
                            last_connected = datetime.datetime.strptime(
                                disk.InstallDate.split('.')[0], 
                                '%Y%m%d%H%M%S'
                            ).strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            pass
                    
                    devices.append({
                        'FriendlyName': disk.Caption,
                        'Serial': serial,
                        'Manufacturer': disk.Manufacturer if disk.Manufacturer else "Unknown",
                        'LastConnectedTime': last_connected,
                        'DetectionMethod': 'WMI'
                    })
                except:
                    continue
                
        except Exception as e:
            print(f"[WMI Error] {str(e)}")
        finally:
            if self._com_initialized:
                import pythoncom
                pythoncom.CoUninitialize()
        return devices

    def _get_usb_devices_registry(self):
        """Registry-based USB detection"""
        devices = []
        try:
            reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            usbstor_key = winreg.OpenKey(
                reg, 
                r"SYSTEM\CurrentControlSet\Enum\USBSTOR",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY
            )
            
            for vendor_idx in range(winreg.QueryInfoKey(usbstor_key)[0]):
                vendor_name = winreg.EnumKey(usbstor_key, vendor_idx)
                vendor_key = winreg.OpenKey(usbstor_key, vendor_name)
                
                for product_idx in range(winreg.QueryInfoKey(vendor_key)[0]):
                    product_name = winreg.EnumKey(vendor_key, product_idx)
                    product_key = winreg.OpenKey(vendor_key, product_name)
                    
                    for instance_idx in range(winreg.QueryInfoKey(product_key)[0]):
                        instance_id = winreg.EnumKey(product_key, instance_idx)
                        instance_key = winreg.OpenKey(product_key, instance_id)
                        
                        # Get device info
                        friendly_name = winreg.QueryValueEx(instance_key, "FriendlyName")[0] \
                            if "FriendlyName" in [winreg.EnumValue(instance_key, i)[0] for i in range(winreg.QueryInfoKey(instance_key)[1])] \
                            else "Unknown"
                        
                        manufacturer = winreg.QueryValueEx(instance_key, "Mfg")[0] \
                            if "Mfg" in [winreg.EnumValue(instance_key, i)[0] for i in range(winreg.QueryInfoKey(instance_key)[1])] \
                            else "Unknown"
                        
                        # Get last connected time
                        last_connected = "Unknown"
                        try:
                            properties_path = rf"SYSTEM\CurrentControlSet\Enum\USBSTOR\{vendor_name}\{product_name}\{instance_id}\Properties\{{83da6326-97a6-4088-9453-a1923f573b29}}\0066"
                            properties_key = winreg.OpenKey(reg, properties_path)
                            last_connected = self.filetime_to_dt(winreg.QueryValueEx(properties_key, "")[0])
                            winreg.CloseKey(properties_key)
                        except:
                            pass
                        
                        devices.append({
                            'FriendlyName': friendly_name,
                            'Serial': instance_id.split('&')[0],
                            'Manufacturer': manufacturer,
                            'LastConnectedTime': last_connected,
                            'DetectionMethod': 'Registry'
                        })
                        
                        winreg.CloseKey(instance_key)
                    winreg.CloseKey(product_key)
                winreg.CloseKey(vendor_key)
            winreg.CloseKey(usbstor_key)
            winreg.CloseKey(reg)
            
        except Exception as e:
            print(f"[Registry Error] {str(e)}")
        
        return devices

    def get_usb_devices(self) -> List[Dict]:
        """Get USB devices with automatic fallback"""
        if not self.is_admin():
            return []

        # Try registry method first
        devices = self._get_usb_devices_registry()
        
        # Fallback to WMI if registry failed
        if not devices:
            devices = self._get_usb_devices_wmi()
        
        return devices