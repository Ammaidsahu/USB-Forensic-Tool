import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtCore import QObject, pyqtSignal
from config import config
import os
from datetime import datetime

class AlertSystem(QObject):
    alert_triggered = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.email_enabled = False
        self.email_settings = {}
        self.load_email_settings()
        
    def load_email_settings(self):
        """Load email settings from environment variables"""
        try:
            self.email_settings = {
                'smtp_server': os.getenv('SMTP_SERVER'),
                'smtp_port': int(os.getenv('SMTP_PORT', 587)),
                'email_from': os.getenv('EMAIL_FROM'),
                'email_password': os.getenv('EMAIL_PASSWORD'),
                'email_to': os.getenv('EMAIL_TO')
            }
            self.email_enabled = all(self.email_settings.values())
        except Exception as e:
            print(f"Error loading email settings: {str(e)}")
            self.email_enabled = False
            
    def send_alert(self, subject, message):
        """Send an alert via email and GUI notification"""
        # Emit signal for GUI notification
        self.alert_triggered.emit(f"{subject}: {message}")
        
        # Send email if enabled
        if self.email_enabled:
            try:
                msg = MIMEMultipart()
                msg['From'] = self.email_settings['email_from']
                msg['To'] = self.email_settings['email_to']
                msg['Subject'] = f"USB Forensic Alert: {subject}"
                
                body = f"""
                USB Forensic Tool Alert
                ----------------------
                Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                {message}
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP(
                    self.email_settings['smtp_server'], 
                    self.email_settings['smtp_port']
                ) as server:
                    server.starttls()
                    server.login(
                        self.email_settings['email_from'], 
                        self.email_settings['email_password']
                    )
                    server.send_message(msg)
                    
                print("Alert email sent successfully")
            except Exception as e:
                print(f"Failed to send alert email: {str(e)}")
                
    def send_suspicious_file_alert(self, file_info):
        """Send an alert about a suspicious file"""
        message = f"""
        Suspicious file detected on USB device!
        
        File Path: {file_info['file_path']}
        File Size: {file_info['file_size']}
        MD5 Hash: {file_info['hash_md5']}
        SHA256 Hash: {file_info['hash_sha256']}
        Timestamp: {file_info['timestamp']}
        """
        
        self.send_alert("Suspicious File Detected", message)
        
    def send_usb_connection_alert(self, device_info, event_type):
        """Send an alert about USB connection/disconnection"""
        action = "connected" if event_type == "CONNECT" else "disconnected"
        
        message = f"""
        USB device {action}!
        
        Device Name: {device_info['device_name']}
        Serial Number: {device_info['serial_number']}
        Manufacturer: {device_info['manufacturer']}
        Storage Capacity: {device_info['storage_capacity']}
        Timestamp: {device_info['timestamp']}
        """
        
        self.send_alert(f"USB Device {action.capitalize()}", message)