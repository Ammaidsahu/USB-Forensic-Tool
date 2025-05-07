# report_generator.py

from fpdf import FPDF
import os

def generate_usb_history_report():
    from usb_history import get_usb_history
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "USB History Report", ln=True, align="C")

    for entry in get_usb_history():
        pdf.multi_cell(0, 10, entry + "\n")

    pdf.output("USB_History_Report.pdf")

def generate_hash_report():
    from hash_utils import compute_hashes_for_usb
    hashes = compute_hashes_for_usb()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "USB Hash Report", ln=True, align="C")
    pdf.multi_cell(0, 10, hashes)

    pdf.output("USB_Hash_Report.pdf")
