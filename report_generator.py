from reportlab.pdfgen import canvas

def generate_pdf(data, filename="usb_report.pdf"):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 12)
    c.drawString(100, 800, "USB Forensic Report")
    y = 770
    for d in data:
        line = f"Device: {d['Device']} | Serial: {d['Serial']} | Name: {d['FriendlyName']}"
        c.drawString(100, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = 770
    c.save()
