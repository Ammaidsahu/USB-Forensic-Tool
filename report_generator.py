from reportlab.pdfgen import canvas

def generate_pdf(data, filename="usb_report.pdf"):
    c = canvas.Canvas(filename)
    c.drawString(100, 800, "USB Forensic Report")
    y = 770
    for d in data:
        c.drawString(100, y, str(d))
        y -= 20
    c.save()