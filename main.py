import tkinter as tk
from usb_scanner import parse_usb_history
from report_generator import generate_pdf

root = tk.Tk()
root.title("USB Forensic Tool")
root.geometry("700x500")

output = tk.Text(root, height=25, width=80)
output.pack(pady=10)

def scan():
    devices = parse_usb_history()
    output.delete("1.0", tk.END)
    for d in devices:
        line = f"Device: {d['Device']} | Serial: {d['Serial']} | LastWrite: {d['LastWrite']} | Name: {d['FriendlyName']}\n"
        output.insert(tk.END, line)

def export():
    devices = parse_usb_history()
    generate_pdf(devices)
    output.insert(tk.END, "\nReport Generated: usb_report.pdf\n")

tk.Button(root, text="Scan USB History", command=scan).pack(pady=5)
tk.Button(root, text="Generate PDF Report", command=export).pack(pady=5)

root.mainloop()