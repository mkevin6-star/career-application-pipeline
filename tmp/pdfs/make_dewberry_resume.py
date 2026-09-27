from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUT = Path("output/pdf/Kevin_Mathews_Dewberry_Survey_Intern_Resume.pdf")


def paragraph(text, style):
    return Paragraph(text, style)


def experience(title, dates, bullets, styles):
    role = paragraph(f"<b>{title}</b>", styles["role"])
    date = paragraph(dates, styles["date"])
    header = Table([[role, date]], colWidths=[4.85 * inch, 1.45 * inch])
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    header.hAlign = "LEFT"
    rows = [header]
    for bullet in bullets:
        rows.append(paragraph(f"&bull; {bullet}", styles["bullet"]))
    rows.append(Spacer(1, 4))
    return KeepTogether(rows)


def section(title, styles):
    return [Spacer(1, 4), paragraph(title.upper(), styles["section"]), Spacer(1, 2)]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT), pagesize=letter,
        leftMargin=0.62 * inch, rightMargin=0.62 * inch,
        topMargin=0.48 * inch, bottomMargin=0.48 * inch,
        title="Kevin Mathews - Dewberry Survey Intern Resume",
        author="Kevin Mathews",
    )
    base = getSampleStyleSheet()["Normal"]
    navy = colors.HexColor("#15324B")
    teal = colors.HexColor("#176B73")
    ink = colors.HexColor("#18232E")
    muted = colors.HexColor("#3F4B55")
    styles = {
        "name": ParagraphStyle("name", parent=base, fontName="Helvetica-Bold", fontSize=19, leading=21, textColor=navy, spaceAfter=2),
        "contact": ParagraphStyle("contact", parent=base, fontName="Helvetica", fontSize=8.7, leading=10.5, textColor=muted),
        "section": ParagraphStyle("section", parent=base, fontName="Helvetica-Bold", fontSize=9.3, leading=11, textColor=teal, tracking=0.7),
        "body": ParagraphStyle("body", parent=base, fontName="Helvetica", fontSize=8.8, leading=11.1, textColor=ink),
        "role": ParagraphStyle("role", parent=base, fontName="Helvetica", fontSize=8.9, leading=11, textColor=ink),
        "date": ParagraphStyle("date", parent=base, fontName="Helvetica", fontSize=8.5, leading=11, alignment=TA_RIGHT, textColor=muted),
        "bullet": ParagraphStyle("bullet", parent=base, fontName="Helvetica", fontSize=8.55, leading=10.75, leftIndent=10, firstLineIndent=-8, textColor=ink),
        "small": ParagraphStyle("small", parent=base, fontName="Helvetica", fontSize=8.45, leading=10.5, textColor=ink),
    }

    story = [
        paragraph("Kevin Mathews", styles["name"]),
        paragraph("Blacksburg, VA  |  (804) 664-5640  |  mkevinj392@gmail.com  |  linkedin.com/in/kevin-mathews-b4958a295", styles["contact"]),
        Spacer(1, 6), HRFlowable(width="100%", thickness=0.7, color=navy),
        *section("Education", styles),
        paragraph("<b>Virginia Tech</b>, Blacksburg, VA", styles["body"]),
        paragraph("B.S. in Computational Modeling and Data Analytics, Concentration in Economics | Expected May 2029 | GPA: 3.6/4.00", styles["body"]),
        paragraph("Relevant coursework: Software Design and Data Structures, Calculus I, Discovering CMDA, Principles of Economics", styles["small"]),
        *section("Technical Skills", styles),
        paragraph("<b>Geospatial and analytical:</b> ArcGIS, Python, SQL, MATLAB, Jupyter Notebook, Microsoft Excel", styles["small"]),
        paragraph("<b>Programming and web:</b> JavaScript, Java, HTML/CSS, Google App Script", styles["small"]),
        paragraph("<b>Focus:</b> Geospatial data visualization, data analysis, web development, IT project management", styles["small"]),
        *section("Relevant Experience", styles),
        experience("Researcher, University of Richmond - Richmond, VA", "Jun 2023 - Aug 2024", [
            "Analyzed Richmond-area air-quality and energy-usage data using ArcGIS.",
            "Built geospatial data visualizations that informed study conclusions on regional energy patterns.",
        ], styles),
        experience("Technology Intern, Virtual School", "Jun 2024 - Aug 2024", [
            "Streamlined an applicant-review process using Google App Script and web-based tools across 160+ hours.",
        ], styles),
        experience("Development Team Member, Center for Information Technology", "Feb 2023 - Aug 2024", [
            "Developed backend and frontend components for a school English Department blog platform using JavaScript, SQL, HTML, and CSS.",
            "Used APIs to build and update website functionality for a client and presented deliverables directly to the client.",
        ], styles),
        *section("Geospatial Leadership and Activities", styles),
        paragraph("&bull; Technology Student Association State Winner - 1st Place, Geospatial Technology. &nbsp;&nbsp; &bull; NASA Virginia Earth and Science Scholar.", styles["bullet"]),
        paragraph("&bull; Computer Club Officer; led sessions on data-science fundamentals using Jupyter Notebook, MATLAB, and Excel. &nbsp;&nbsp; &bull; Competed in data science, web development, and geospatial technology events, 2021-2024.", styles["bullet"]),
        *section("Additional Experience", styles),
        experience("Assistant Track Coach, Future Flyers (nonprofit)", "Mar 2024 - Aug 2024", [
            "Organized practices alongside coaching staff and supported student-athletes at track meets; completed 50+ volunteer hours.",
        ], styles),
    ]
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
