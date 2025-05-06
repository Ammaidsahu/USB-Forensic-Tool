import os
import json
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DATABASE = {
    'name': 'usb_forensics.db',
    'path': os.path.join(BASE_DIR, 'usb_forensics.db')
}

# Report configuration
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

# File monitoring
MONITORED_EXTENSIONS = ['.exe', '.dll', '.bat', '.ps1', '.vbs', '.js']
SUSPICIOUS_KEYWORDS = ['malware', 'virus', 'trojan', 'ransomware', 'keylogger']

# UI Settings
UI_THEME = os.path.join(BASE_DIR, 'assets', 'styles', 'forensic_theme.qss')
ICON_PATH = os.path.join(BASE_DIR, 'assets', 'icons')


class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self):
        """Load configuration from a JSON file."""
        if not os.path.exists(self.config_file):
            return self._create_default_config()

        with open(self.config_file, "r") as f:
            return json.load(f)

    def _create_default_config(self):
        """Create a default configuration."""
        default_config = {
            "usb_monitoring_enabled": True,
            "file_monitoring_enabled": True,
            "report_storage_path": "reports/",
            "log_level": "INFO",
            "auto_start_on_boot": True,
        }

        self._save_config(default_config)
        return default_config

    def _save_config(self, config_data):
        """Save the current configuration to a JSON file."""
        with open(self.config_file, "w") as f:
            json.dump(config_data, f, indent=4)

    def get(self, key):
        """Get the configuration value for a specific key."""
        return self.config_data.get(key)

    def set(self, key, value):
        """Set the configuration value for a specific key."""
        self.config_data[key] = value
        self._save_config(self.config_data)


if __name__ == "__main__":
    # Example usage
    config = Config()
    print(config.get("report_storage_path"))  # Print the report storage path
    config.set("log_level", "DEBUG")  # Change the log level
