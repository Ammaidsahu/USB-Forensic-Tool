# 🔍 USB Forensic Tool

A modern USB Forensic Tool developed by final-year Computer Engineering students to monitor USB activity in real time, retrieve complete device metadata, track file transfers, calculate file hashes, and generate NIST-compliant forensic reports. Built using **PyQt5** with a sleek digital forensics-themed interface, this tool is ideal for investigators, forensic analysts, and cybersecurity researchers.

---

## 📌 Features

- 🔌 Detect all USB and external storage devices connected to the system  
- 🕵️ Retrieve device metadata: Serial Number, Manufacturer, Vendor ID, Capacity, First/Last Seen  
- ⚙️ Live monitoring of USB insertions/removals  
- 📂 Real-time tracking of file creation, deletion, and transfers on USB drives  
- 🧮 File hash calculation using MD5 and SHA-256  
- 📝 Generate detailed PDF reports for digital investigations  
- 🖥️ Professional GUI built with PyQt5  
- 🔁 Runs silently in the background on system startup (auto-run feature)  

---

## 🖥️ System Requirements

- **Operating System:** Windows 10 or later (Admin rights required)  
- **Python Version:** Python 3.8+  
- **Permissions:** Admin privileges for registry and file system monitoring  

---

## 🧰 Tools & Libraries Used

| Purpose                 | Tool/Library        |
|------------------------|---------------------|
| Programming Language   | Python 3            |
| GUI Framework          | PyQt5               |
| USB Device Metadata    | pyudev, winreg, wmi |
| Real-Time Monitoring   | watchdog, pywin32   |
| Report Generation      | reportlab           |
| Background Service     | pywin32, winshell   |
| File Hashing           | hashlib             |
| Database Logging       | sqlite3             |

---

## 📦 Installation

Install the required dependencies:


pip install pyqt5 watchdog pywin32 wmi reportlab

🗂️ Project Structure

USB_Forensic_Tool/
│
├── main.py                 # App launcher
├── gui.py                  # PyQt5 GUI code
├── usb_monitor.py          # Detects USB insert/removal
├── usb_history.py          # Scans registry for past USB devices
├── file_monitor.py         # Monitors file operations on USB drives
├── hash_utils.py           # Calculates MD5 and SHA256 of files
├── report_generator.py     # Generates forensic PDF reports
├── background_service.py   # Enables auto-start on system boot
├── assets/                 # App icons and themed images
├── database/usb_logs.db    # SQLite database for log storage
├── config.py               # App configuration
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation

🚀 Getting Started

📥 Clone the Repository

git clone https://github.com/yourusername/usb-forensic-tool.git
cd usb-forensic-tool

▶️ Run the Application

python main.py

🧭 GUI Guide

| Button / Tab    | Description                                                    |
| --------------- | -------------------------------------------------------------- |
| Live Logging    | Starts real-time detection of USB plug/unplug and file actions |
| USB History     | Shows all previously connected USB devices with metadata       |
| File Transfers  | Logs file creation, copy, delete events on USB                 |
| Hash Calculator | Calculates and compares MD5/SHA256 file hashes                 |
| Generate Report | Exports investigation log into a PDF document                  |

🧪 Testing
| Test Case             | Expected Outcome                               |
| --------------------- | ---------------------------------------------- |
| Connect USB Device    | Device is detected and shown in Live Log       |
| Copy file to/from USB | File path and action are logged                |
| Run USB History       | Lists past connected USB devices with metadata |
| Calculate Hash        | Correct MD5/SHA256 hash values generated       |
| Generate Report       | Creates downloadable PDF with evidence logs    |
| Remove USB Device     | Disconnect event shown in GUI                  |

📈 Future Enhancements

📊 Timeline view of USB events

🚨 Email/SMS alert on suspicious USB actions

🔐 USB device blocking via admin panel

🧠 AI-based anomaly detection on file behavior

🌐 Cloud syncing for remote investigation

⚖️ License

This project is licensed under the MIT License.
Use freely for research, education, or internal forensic investigation purposes.

📬 Contact

For collaboration, issues, or academic inquiries:

📧 Ammaidsahu8@gmail.com

🏫 Cyber Security – FCSE, GIKI
