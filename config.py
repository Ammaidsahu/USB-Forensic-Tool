# config.py
SMTP = {
    'server': 'smtp.gmail.com',
    'port': 587,
    'user': 'Ammaidsahu8@gmail.com',
    'password': os.getenv('Ammaid.sahu8'),  # From environment variables
    'sender': 'usb-monitor@company.com',
    'recipient': 'security-team@company.com'
}

DB_CONFIG = {
    'path': '/secure/usb_forensics.db',
    'backup_interval': 3600  # 1 hour
}

ALERT_RULES = {
    'new_device': True,
    'suspicious_files': True,
    'whitelist': ['1234567890']  # Known good serials
}