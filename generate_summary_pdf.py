"""
Generator script to compile Product_Manual_Summary.md into a professional 5-10 page PDF.
Uses ReportLab with custom styles, headers, footers, tables, and page numbering.
"""
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas subclass to dynamically compute and draw running headers and footers with total page counts.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            # Suppress header/footer on title page
            return
        
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Header
        self.drawString(54, 11 * 72 - 36, "HP Laser 100 Series Printer — Executive Product Manual Summary")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer
        self.line(54, 50, 8.5 * 72 - 54, 50)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — FOR INTERNAL USE")
        self.restoreState()

def create_pdf():
    pdf_path = Path("Product_Manual_Summary.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Define custom document typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=15,
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=8,
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4,
    )

    tbl_header_style = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white,
    )

    tbl_body_style = ParagraphStyle(
        'TblBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#2D3748"),
    )

    story = []

    # Title Banner Block
    story.append(Paragraph("HP Laser 100 Series Printer User Guide", title_style))
    story.append(Paragraph("Executive Product Manual Summary | Models: HP Laser 103, 107, 108 Series", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2B6CB0"), spaceAfter=15))

    # SECTION 1
    story.append(Paragraph("1. Product Overview & Key Benefits", h1_style))
    story.append(Paragraph(
        "The <b>HP Laser 100 Series</b> (including HP Laser 103, 107, and 108) is an ultra-compact monochrome laser printer series designed for personal, home office, and small business productivity. It engineered for users requiring fast, crisp black-and-white text printing with simple setup and maintenance.",
        body_style
    ))
    story.append(Paragraph("<b>Core Features & Operational Advantages:</b>", h2_style))
    story.append(Paragraph("• <b>High Output Performance</b>: Print speeds up to 20 ppm (A4) / 21 ppm (Letter) with a quick First Page Out Time (FPOT) of under 8.3 seconds.", bullet_style))
    story.append(Paragraph("• <b>Space-Saving Chassis</b>: Highly compact dimensions allowing desk placement in tight office spaces.", bullet_style))
    story.append(Paragraph("• <b>Energy & Eco Efficiency</b>: Integrated Auto-Off / Power Save modes substantially lower power draw when idle. Supports recycled paper stock and multi-page N-up printing to minimize paper waste.", bullet_style))
    story.append(Paragraph("• <b>Flexible Wireless & Mobile Printing</b>: Select models (107w / 108w) support Wi-Fi 802.11b/g/n, Wi-Fi Direct, Apple AirPrint, and the HP Smart Application.", bullet_style))
    story.append(Spacer(1, 10))

    # SECTION 2
    story.append(Paragraph("2. Important Safety Precautions & Information", h1_style))
    story.append(Paragraph(
        "Adhering to safety rules is essential to ensure user protection, avoid operational risks, and prevent damage to internal mechanical assemblies.",
        body_style
    ))
    story.append(Paragraph("• <b>Electrical & Power Safety</b>: Connect exclusively to grounded AC wall outlets matching the rated voltage (110V or 220V). Unplug the machine before cleaning internal components.", bullet_style))
    story.append(Paragraph("• <b>Fuser Thermal Precautions</b>: The fuser operating zone reaches high temperatures during printing. Always allow the fuser to cool before opening internal covers or clearing paper jams.", bullet_style))
    story.append(Paragraph("• <b>Toner Safety & Washing Rules</b>: Do not inhale toner powder or incinerate cartridges. Wash exposed skin with cold water immediately if toner contacts skin or clothes.", bullet_style))
    story.append(Paragraph("• <b>Environment & Ventilation Placement</b>: Place on a sturdy, level surface with at least 10–15 cm clearance around ventilation openings to prevent thermal overheating.", bullet_style))
    story.append(Spacer(1, 10))

    story.append(PageBreak()) # Clean page break for multi-page document structure

    # SECTION 3
    story.append(Paragraph("3. Hardware & Software Installation & Setup", h1_style))
    story.append(Paragraph("<b>3.1 Initial Unboxing & Cartridge Installation</b>", h2_style))
    story.append(Paragraph("1. Unpack all shipping tape, protective plastic film, and internal packing foam from the printer body.", bullet_style))
    story.append(Paragraph("2. Open the top cover, extract the pre-installed toner cartridge, and gently rock it side-to-side 5 to 6 times to distribute toner evenly.", bullet_style))
    story.append(Paragraph("3. Reinsert the cartridge into the guides until locked in position, then close the top cover.", bullet_style))
    story.append(Paragraph("4. Connect the power cable securely and turn on the machine using the control panel power button.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3.2 Driver Installation & Connectivity</b>", h2_style))
    story.append(Paragraph("• <b>Windows OS (7 / 8 / 10 / 11)</b>: Download the driver package from www.hp.com/support/laser100. Run installer software and connect the USB cable only when prompted by the wizard.", bullet_style))
    story.append(Paragraph("• <b>Mac OS & AirPrint</b>: Mac OS X 10.7+ supports native driverless printing via Apple AirPrint. Add the printer via System Preferences > Printers & Scanners.", bullet_style))
    story.append(Paragraph("• <b>WPS Wireless Setup</b>: Press and hold the Wireless button for 10 seconds until the LED blinks, then press the WPS button on your router within 2 minutes.", bullet_style))
    story.append(Spacer(1, 10))

    # SECTION 4
    story.append(Paragraph("4. Media & Paper Handling Specifications", h1_style))
    story.append(Paragraph("<b>4.1 Media Types & Capacity Ratings</b>", h2_style))
    story.append(Paragraph("• <b>Supported Media Types</b>: Plain paper, Heavyweight, Recycled, Preprinted, Labels, Envelopes, Bond, Cardstock.", bullet_style))
    story.append(Paragraph("• <b>Input Capacity</b>: Main tray holds up to 150 sheets of 80 g/m² plain paper.", bullet_style))
    story.append(Paragraph("• <b>Output Capacity</b>: Output bin holds up to 100 sheets face-down.", bullet_style))
    story.append(Spacer(1, 6))

    # Table for Media Specs
    media_data = [
        [Paragraph("Media Type", tbl_header_style), Paragraph("Supported Dimensions", tbl_header_style), Paragraph("Paper Weight Range", tbl_header_style), Paragraph("Tray Capacity", tbl_header_style)],
        [Paragraph("Plain / Recycled", tbl_body_style), Paragraph("Letter, Legal, A4, A5, Oficio", tbl_body_style), Paragraph("60 to 90 g/m² (16–24 lb)", tbl_body_style), Paragraph("150 Sheets", tbl_body_style)],
        [Paragraph("Heavy / Bond", tbl_body_style), Paragraph("Letter, Legal, A4", tbl_body_style), Paragraph("90 to 120 g/m² (24–32 lb)", tbl_body_style), Paragraph("10–15 Sheets", tbl_body_style)],
        [Paragraph("Envelopes", tbl_body_style), Paragraph("Com10, DL, C5, Monarch", tbl_body_style), Paragraph("75 to 90 g/m²", tbl_body_style), Paragraph("10 Envelopes", tbl_body_style)],
        [Paragraph("Labels / Cardstock", tbl_body_style), Paragraph("Letter, A4", tbl_body_style), Paragraph("Up to 163 g/m² (43 lb)", tbl_body_style), Paragraph("10 Sheets", tbl_body_style)],
    ]

    t_media = Table(media_data, colWidths=[110, 150, 130, 114])
    t_media.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_media)
    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # SECTION 5
    story.append(Paragraph("5. Device Control Panel & Operations", h1_style))
    story.append(Paragraph("The control panel provides physical status push-buttons and LED diagnostic lights:", body_style))

    cp_data = [
        [Paragraph("Control Element", tbl_header_style), Paragraph("LED State / Action", tbl_header_style), Paragraph("Operational Status / Meaning", tbl_header_style)],
        [Paragraph("Power LED / Button", tbl_body_style), Paragraph("Solid White", tbl_body_style), Paragraph("Printer power ON and ready.", tbl_body_style)],
        [Paragraph("Power LED", tbl_body_style), Paragraph("Slow Blinking", tbl_body_style), Paragraph("Power Save mode active or printing data.", tbl_body_style)],
        [Paragraph("Resume / Cancel", tbl_body_style), Paragraph("Hold 10 Seconds", tbl_body_style), Paragraph("Prints Configuration & Network Report.", tbl_body_style)],
        [Paragraph("Resume / Cancel", tbl_body_style), Paragraph("Hold 15 Seconds", tbl_body_style), Paragraph("Prints Supplies Information Report.", tbl_body_style)],
        [Paragraph("Toner LED", tbl_body_style), Paragraph("Blinking Orange", tbl_body_style), Paragraph("Toner low; replacement cartridge recommended.", tbl_body_style)],
        [Paragraph("Toner LED", tbl_body_style), Paragraph("Solid Orange", tbl_body_style), Paragraph("Toner very low/depleted.", tbl_body_style)],
        [Paragraph("Error LED", tbl_body_style), Paragraph("Solid Orange", tbl_body_style), Paragraph("Paper jam, door open, or paper out.", tbl_body_style)],
    ]

    t_cp = Table(cp_data, colWidths=[130, 130, 244])
    t_cp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_cp)
    story.append(Spacer(1, 15))

    # SECTION 6
    story.append(Paragraph("6. Maintenance & Component Care", h1_style))
    story.append(Paragraph("<b>6.1 Replacing the Toner Cartridge</b>", h2_style))
    story.append(Paragraph("1. Turn off the printer power and open the top cover.", bullet_style))
    story.append(Paragraph("2. Pull the used cartridge upward out of the printer.", bullet_style))
    story.append(Paragraph("3. Unpack the new HP toner cartridge, remove all orange shipping shields and sealing tape.", bullet_style))
    story.append(Paragraph("4. Rock the cartridge 5 to 6 times horizontally, then push firmly into the machine until seated.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>6.2 Internal Cleaning</b>", h2_style))
    story.append(Paragraph("1. Unplug the power cable and allow fuser to cool.", bullet_style))
    story.append(Paragraph("2. Wipe down the interior cartridge bay with a dry, lint-free cloth to clear paper dust and loose toner.", bullet_style))
    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # SECTION 7
    story.append(Paragraph("7. Troubleshooting Guide", h1_style))
    story.append(Paragraph("Use the matrix below to resolve operational errors:", body_style))

    tb_data = [
        [Paragraph("Symptom / Problem", tbl_header_style), Paragraph("Probable Cause", tbl_header_style), Paragraph("Solution & Action", tbl_header_style)],
        [Paragraph("Paper Jam in Tray", tbl_body_style), Paragraph("Misaligned stack or overloaded tray.", tbl_body_style), Paragraph("Gently pull jammed media straight out. Do not overload tray above maximum line.", tbl_body_style)],
        [Paragraph("Paper Jam in Fuser", tbl_body_style), Paragraph("Paper path restriction.", tbl_body_style), Paragraph("Cool fuser. Remove toner cartridge and gently pull paper out toward output tray.", tbl_body_style)],
        [Paragraph("Faded Print / Low Quality", tbl_body_style), Paragraph("Uneven toner distribution.", tbl_body_style), Paragraph("Remove cartridge and gently rock side-to-side. Replace cartridge if toner is depleted.", tbl_body_style)],
        [Paragraph("Wireless Connection Failure", tbl_body_style), Paragraph("Router SSID or IP conflict.", tbl_body_style), Paragraph("Re-verify router IP. Print Network Configuration report to confirm SSID matching.", tbl_body_style)],
    ]

    t_tb = Table(tb_data, colWidths=[140, 140, 224])
    t_tb.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_tb)
    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # SECTION 8
    story.append(Paragraph("8. Technical Specifications", h1_style))
    
    spec_data = [
        [Paragraph("Technical Parameter", tbl_header_style), Paragraph("Specification Value", tbl_header_style)],
        [Paragraph("Physical Dimensions (W x D x H)", tbl_body_style), Paragraph("331 x 215 x 178 mm (13.03 x 8.46 x 7.01 in)", tbl_body_style)],
        [Paragraph("Net Device Weight", tbl_body_style), Paragraph("4.18 kg (9.22 lbs)", tbl_body_style)],
        [Paragraph("Print Speed", tbl_body_style), Paragraph("Up to 20 ppm (A4) / 21 ppm (Letter)", tbl_body_style)],
        [Paragraph("Print Resolution", tbl_body_style), Paragraph("Up to 1200 x 1200 dpi effective output", tbl_body_style)],
        [Paragraph("Monthly Duty Cycle", tbl_body_style), Paragraph("Up to 10,000 pages (Recommended: 100 to 1,500 pages)", tbl_body_style)],
        [Paragraph("Processor Speed", tbl_body_style), Paragraph("400 MHz", tbl_body_style)],
        [Paragraph("Power Requirements", tbl_body_style), Paragraph("110V: 110–127 VAC, 50/60 Hz; 220V: 220–240 VAC, 50/60 Hz", tbl_body_style)],
        [Paragraph("Power Consumption", tbl_body_style), Paragraph("Active Print: ~320W, Ready Mode: ~33W, Power Save: ~1.1W", tbl_body_style)],
        [Paragraph("Operating Temperature", tbl_body_style), Paragraph("10°C to 30°C (50°F to 86°F)", tbl_body_style)],
        [Paragraph("Operating Humidity Range", tbl_body_style), Paragraph("20% to 80% Relative Humidity (non-condensing)", tbl_body_style)],
        [Paragraph("Supported Operating Systems", tbl_body_style), Paragraph("Windows 7 / 8 / 10 / 11, macOS 10.7 or newer", tbl_body_style)],
    ]

    t_spec = Table(spec_data, colWidths=[200, 304])
    t_spec.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_spec)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated at: {pdf_path.resolve()}")

if __name__ == "__main__":
    create_pdf()
