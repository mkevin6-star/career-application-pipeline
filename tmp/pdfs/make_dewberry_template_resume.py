from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUT = Path("output/pdf/Kevin_Mathews_Dewberry_Survey_Intern_Resume_Approved_Template.pdf")


def p(text, style):
    return Paragraph(text, style)


def section(label, styles):
    return [Spacer(1, 6), p(label, styles["section"]), HRFlowable(width="100%", thickness=0.55, color=colors.black), Spacer(1, 3)]


def entry(left, right, bullets, styles):
    table = Table([[p(left, styles["entry"]), p(right, styles["date"])]], colWidths=[5.25 * inch, 1.45 * inch])
    table.hAlign = "LEFT"
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    content = [table]
    content.extend(p(f"&bull; {b}", styles["bullet"]) for b in bullets)
    content.append(Spacer(1, 4))
    return KeepTogether(content)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT), pagesize=letter,
        leftMargin=0.58 * inch, rightMargin=0.58 * inch,
        topMargin=0.46 * inch, bottomMargin=0.42 * inch,
        title="Kevin Mathews - Dewberry Survey Intern Resume",
        author="Kevin Mathews",
    )
    normal = getSampleStyleSheet()["Normal"]
    styles = {
        "name": ParagraphStyle("name", parent=normal, fontName="Times-Bold", fontSize=20, leading=22, alignment=TA_CENTER, spaceAfter=1),
        "contact": ParagraphStyle("contact", parent=normal, fontName="Times-Roman", fontSize=9.6, leading=11.4, alignment=TA_CENTER),
        "section": ParagraphStyle("section", parent=normal, fontName="Times-Roman", fontSize=11.6, leading=13.2, alignment=TA_LEFT, spaceAfter=1),
        "entry": ParagraphStyle("entry", parent=normal, fontName="Times-Roman", fontSize=9.75, leading=11.8),
        "date": ParagraphStyle("date", parent=normal, fontName="Times-Roman", fontSize=9.75, leading=11.8, alignment=TA_RIGHT),
        "bullet": ParagraphStyle("bullet", parent=normal, fontName="Times-Roman", fontSize=9.45, leading=11.3, leftIndent=19, firstLineIndent=-10),
        "skills": ParagraphStyle("skills", parent=normal, fontName="Times-Roman", fontSize=9.45, leading=11.3),
    }

    story = [
        p("Kevin Mathews", styles["name"]),
        p("Blacksburg, VA  |  (804) 664-5640  |  mkevinj392@gmail.com  |  linkedin.com/in/kevin-mathews-b4958a295", styles["contact"]),
        *section("EDUCATION", styles),
        entry("<b>Virginia Tech</b>, Blacksburg, VA", "Expected May 2029", [
            "B.S. in Computational Modeling and Data Analytics, Concentration in Economics | GPA: 3.6/4.00",
            "Relevant coursework: Software Design and Data Structures, Calculus I, Discovering CMDA, Principles of Economics",
        ], styles),
        *section("EXPERIENCE", styles),
        entry("<b>University of Richmond</b>, Researcher, Richmond, VA", "Jun 2023 - Aug 2024", [
            "Analyzed Richmond-area air-quality and energy-usage data using ArcGIS.",
            "Built geospatial data visualizations that informed study conclusions on regional energy patterns.",
        ], styles),
        entry("<b>Virtual School</b>, Technology Intern", "Jun 2024 - Aug 2024", [
            "Streamlined an applicant-review process using Google App Script and web-based tools across 160+ hours.",
        ], styles),
        entry("<b>Center for Information Technology</b>, Development Team Member", "Feb 2023 - Aug 2024", [
            "Developed backend and frontend components for a school English Department blog platform using JavaScript, SQL, HTML, and CSS.",
            "Used APIs to build and update website functionality for a client and presented deliverables directly to the client.",
        ], styles),
        *section("LEADERSHIP AND RELEVANT EXPERIENCE", styles),
        entry("<b>Technology Student Association</b>, State Winner - 1st Place, Geospatial Technology", "", [
            "Recognized for geospatial technology work in statewide competition.",
        ], styles),
        entry("<b>Computer Club</b>, Officer", "", [
            "Led sessions on data-science fundamentals using Jupyter Notebook, MATLAB, and Excel.",
        ], styles),
        entry("<b>Future Flyers (nonprofit)</b>, Assistant Track Coach", "Mar 2024 - Aug 2024", [
            "Organized practices alongside coaching staff and supported student-athletes at track meets; completed 50+ volunteer hours.",
        ], styles),
        *section("SKILLS", styles),
        p("Geospatial and analytical: ArcGIS, Python, SQL, MATLAB, Jupyter Notebook, Microsoft Excel", styles["skills"]),
        p("Programming and web: JavaScript, Java, HTML/CSS, Google App Script", styles["skills"]),
        p("Focus: Geospatial data visualization, data analysis, web development, IT project management", styles["skills"]),
    ]
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
