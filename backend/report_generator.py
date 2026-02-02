from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_report(data, filename="financial_report.pdf"):

    styles = getSampleStyleSheet()
    elements = []

    doc = SimpleDocTemplate(filename)

    elements.append(Paragraph("Financial Health Report", styles["Heading1"]))
    elements.append(Spacer(1, 20))

    for k, v in data.items():
        if isinstance(v, (int, float, str)):
            elements.append(
                Paragraph(f"{k}: {v}", styles["Normal"])
            )

    doc.build(elements)

    return filename
