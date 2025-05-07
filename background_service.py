# background_service.py

import subprocess

def enable_auto_start():
    import os
    import sys
    startup = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    script = os.path.join(startup, "usb_monitor.bat")
    with open(script, "w") as f:
        f.write(f"python {os.path.abspath('main.py')}")
