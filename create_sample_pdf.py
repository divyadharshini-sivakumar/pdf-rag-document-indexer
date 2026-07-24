"""
Utility script to generate a synthetic product manual PDF for Lab 1 testing.
"""
from pathlib import Path

def generate_sample_pdf():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError as e:
        print(f"[ERROR] ReportLab is required to generate the sample PDF: {e}")
        return

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    pdf_path = data_dir / "sample_product_manual.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    
    sections = [
        ("Safety & Warnings", "Always disconnect main power before servicing the unit. Wear protective gloves and eye protection."),
        ("Installation Requirements", "Ensure adequate ventilation space of at least 15 cm around the chassis. Mount on a flat, non-flammable surface."),
        ("Operating Instructions", "To turn on the system, switch the primary breaker to ON. Wait for the green LED indicator before initiating operational cycles."),
        ("Troubleshooting Guide", "If Error Code E-102 appears, inspect thermal sensors and clear any blockage from cooling intakes."),
        ("Maintenance & Care", "Clean air filters every 30 days using compressed air. Inspect power cables annually for signs of wear.")
    ]

    page_num = 1
    # Generate 50 pages of sample content
    for repeat in range(10):
        for title, content in sections:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, f"{title} (Part {repeat + 1})")
            c.setFont("Helvetica", 12)
            c.drawString(50, 720, f"Page {page_num} of Product Manual v2.4")
            
            text_object = c.beginText(50, 680)
            text_object.setFont("Helvetica", 10)
            for line in [content] * 5:
                text_object.textLine(line)
            c.drawText(text_object)
            
            c.showPage()
            page_num += 1

    c.save()
    print(f"[SUCCESS] Created synthetic sample manual at: {pdf_path.resolve()}")

if __name__ == "__main__":
    generate_sample_pdf()
