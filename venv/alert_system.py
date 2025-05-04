import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class AlertSystem:
    def __init__(self):
        self.smtp_config = {
            'server': 'smtp.gmail.com',
            'port': 587,
            'user': 'ammaidsahu8@gmail.com',
            'password': os.getenv('GMAIL_APP_PASSWORD'),  # From environment variable
            'sender': 'ammaidsahu8@gmail.com',
            'recipient': 'ammaidsahu8@gmail.com'
        }

    def check_new_device(self, serial):
        if serial == "UNKNOWN":
            self.send_alert("⚠️ Unknown USB Device Detected", 
                          f"An unidentifiable USB device was connected:\n\nSerial: {serial}")

    def send_alert(self, subject, body):
        if not self.smtp_config['password']:
            print("Gmail app password not configured - skipping email alert")
            return

        def _send():
            try:
                msg = MIMEMultipart()
                msg['From'] = self.smtp_config['sender']
                msg['To'] = self.smtp_config['recipient']
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                    server.starttls()
                    server.login(self.smtp_config['user'], self.smtp_config['password'])
                    server.send_message(msg)
                    print("Alert email sent successfully")
            except Exception as e:
                print(f"Failed to send alert: {str(e)}")

        threading.Thread(target=_send, daemon=True).start()