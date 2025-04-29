# 🔍 USB Forensic Tool

A lightweight and efficient USB Forensic Tool developed by final-year computer engineering students to extract USB device metadata, monitor live USB events, track file transfers, and generate investigation-ready reports. Ideal for digital forensics analysts and cybersecurity researchers.

---

## 📌 Features

- 🔌 Detect all USB devices ever connected to the system
- 🕵️ Retrieve metadata: Serial Number, Manufacturer, Last Connected Time
- ⚙️ Live USB connection/disconnection monitoring
- 📂 Detect real-time file transfers to/from USB
- 📝 Export forensic findings as a detailed PDF report
- 🧑‍💻 Easy-to-use graphical interface using Tkinter

---

## 🖥️ System Requirements

- **Operating System:** Windows 10 or later
- **Python Version:** Python 3.8+
- **Admin Rights:** Required to access Windows registry

---

## 🧰 Tools & Libraries Used

| Purpose               | Tool/Library         |
|----------------------|----------------------|
| Programming Language | Python 3             |
| GUI Interface        | Tkinter              |
| Registry Parsing     | python-registry, regipy |
| USB Event Monitor    | pywin32              |
| File Monitoring      | watchdog             |
| Report Generation    | reportlab            |

Install required dependencies:
```bash
pip install pywin32 regipy python-registry watchdog reportlab
🗂️ Project Structure
graphql
Copy
Edit
USB_Forensic_Tool/
│
├── main.py                 # GUI and application controller
├── usb_scanner.py          # Registry-based USB history extractor
├── usb_monitor.py          # Real-time USB connection detector
├── file_monitor.py         # File transfer monitor for USB drives
├── report_generator.py     # Generate detailed PDF reports
├── database.db             # (Optional) Log event data in SQLite
├── README.md               # Project documentation
└── assets/                 # Icons, logos, or GUI elements
🚀 Getting Started
Clone the repository
git clone https://github.com/yourusername/usb-forensic-tool.git
cd usb-forensic-tool
Run the application
python main.py
Use the GUI

📌 Click "Scan USB History" to extract past USB device logs

⚙️ Start monitoring real-time USB activity

📂 Track file transfers to/from USB drives

📝 Generate a professional PDF report


🧪 Testing

Test Case	Expected Outcome
Connect USB Device	Detected and listed in GUI
File copied to USB	File path appears in monitor
Report Generation	Creates a PDF with device + file logs
Unplug USB	Event shown in live log
📈 Future Enhancements
Cross-platform (Linux/macOS) support

Timeline visualization of USB events

Hashing & integrity check of transferred files

Email alert on suspicious USB activity


⚖️ License
This project is licensed under the MIT License.

📬 Contact
For inquiries or academic collaboration:
📧 Ammaidsahu8"gmail.com
🏫 Cyber Security , FCSE , GIKI
