from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from database import USBForensicDB
import time

def generate_pdf(devices, filename="usb_report.pdf"):
    db = USBForensicDB()
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "USB Forensic Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Generated on: {time.ctime()}")
    
    # Device Summary
    y_position = 700
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_position, "Connected USB Devices:")
    y_position -= 20
    
    device_data = [['Serial', 'Manufacturer', 'First Seen', 'Last Seen']]
    for device in devices:
        history = db.get_device_history(device['Serial'])
        if history:
            device_data.append([
                history[1],  # serial
                history[2],  # manufacturer
                history[3],  # first_seen
                history[4]   # last_seen
            ])
    
    # Create table
    table = Table(device_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    
    table.wrapOn(c, 400, 200)
    table.drawOn(c, 100, y_position - len(device_data)*20)
    
    # File Events
    y_position -= len(device_data)*20 + 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_position, "File Events:")
    y_position -= 20
    
    for device in devices:
        history = db.get_device_history(device['Serial'])
        if history:
            events = db.get_file_events(history[0])  # device_id
            if events:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, y_position, f"Device: {device['Serial']}")
                y_position -= 15
                
                event_data = [['Timestamp', 'Event', 'File', 'Size (MB)', 'Hash']]
                for event in events[:10]:  # Show last 10 events
                    event_data.append([
                        event[6],  # timestamp
                        event[2],  # event_type
                        event[3],  # file_path
                        f"{event[4]:.2f}",  # file_size
                        event[5][:8] + "..."  # abbreviated hash
                    ])
                
                event_table = Table(event_data)
                event_table.setStyle(TableStyle([
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 10),
                    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
                ]))
                
                event_table.wrapOn(c, 450, 100)
                event_table.drawOn(c, 100, y_position - len(event_data)*15)
                y_position -= len(event_data)*15 + 30
    
    c.save()