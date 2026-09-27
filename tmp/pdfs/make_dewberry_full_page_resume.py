from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUT = Path("output/pdf/Kevin_Mathews_Dewberry_Survey_Intern_Resume_Full_Page.pdf")


def p(text, style):
    return Paragraph(text, style)


def section(label, styles):
    return [Spacer(1, 5), p(label, styles["section"]), HRFlowable(width="100%", thickness=0.55, color=colors.black), Spacer(1, 2)]


def entry(left, right, bullets, styles):
    header = Table([[p(left, styles["entry"]), p(right, styles["date"])]], colWidths=[5.35 * inch, 1.65 * inch])
    header.hAlign = "LEFT"
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    content = [header]
    content.extend(p(f"&bull; {bullet}", styles["bullet"]) for bullet in bullets)
    content.append(Spacer(1, 3))
    return KeepTogether(content)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT), pagesize=letter,
        leftMargin=0.5 * inch, rightMargin=0.5 * inch,
        topMargin=0.48 * inch, bottomMargin=0.44 * inch,
        title="Kevin Mathews - Dewberry Survey Intern Resume",
        author="Kevin Mathews",
    )
    base = getSampleStyleSheet()["Normal"]
    styles = {
        "name": ParagraphStyle("name", parent=base, fontName="Times-Bold", fontSize=20, leading=22, alignment=TA_CENTER, spaceAfter=1),
        "contact": ParagraphStyle("contact", parent=base, fontName="Times-Roman", fontSize=9.6, leading=11.4, alignment=TA_CENTER),
        "section": ParagraphStyle("section", parent=base, fontName="Times-Roman", fontSize=11.6, leading=13.2, alignment=TA_LEFT, spaceAfter=1),
        "entry": ParagraphStyle("entry", parent=base, fontName="Times-Roman", fontSize=9.65, leading=11.45),
        "date": ParagraphStyle("date", parent=base, fontName="Times-Roman", fontSize=9.65, leading=11.45, alignment=TA_RIGHT),
        "bullet": ParagraphStyle("bullet", parent=base, fontName="Times-Roman", fontSize=9.35, leading=10.95, leftIndent=19, firstLineIndent=-10),
        "skills": ParagraphStyle("skills", parent=base, fontName="Times-Roman", fontSize=9.35, leading=10.95),
    }
    story = [
        p("Kevin Mathews", styles["name"]),
        p("Blacksburg, VA  |  (804) 664-5640  |  mkevinj392@gmail.com  |  linkedin.com/in/kevin-mathews-b4958a295", styles["contact"]),
        *section("EDUCATION", styles),
        entry("<b>Virginia Tech</b>, Blacksburg, VA", "Expected May 2029", [
            "B.S. in Computational Modeling and Data Analytics (CMDA), Concentration in Economics | GPA: 3.6/4.00",
            "Relevant coursework: Software Design and Data Structures, Calculus I, Discovering CMDA, Principles of Economics",
        ], styles),
        entry("<b>Deep Run High School, Center for Information Technology</b>, Glen Allen, VA", "May 2025", [
            "Technology Student Association State Winner - 1st Place, Geospatial Technology",
            "Relevant coursework: AP Computer Science A, Web Design and Development, IT Project Management, AP Research",
        ], styles),
        *section("EXPERIENCE", styles),
        entry("<b>University of Richmond</b>, Researcher, Richmond, VA", "Jun 2023 - Aug 2024", [
            "Collaborated with a University of Richmond professor on a study of the Richmond, VA area.",
            "Analyzed air-quality and energy-usage data using ArcGIS.",
            "Built geospatial data visualizations that informed the study's conclusions on regional energy patterns.",
        ], styles),
        entry("<b>Center for Information Technology</b>, Development Team Member", "Feb 2024 - Aug 2024", [
            "Developed the backend of a school English Department blog platform using JavaScript and SQL.",
            "Developed frontend components using HTML, CSS, and JavaScript.",
        ], styles),
        entry("<b>Center for Information Technology</b>, Development Team Member", "Feb 2023 - Apr 2023", [
            "Used APIs to build and update website functionality for a client, Woodland Cemetery.",
            "Presented project deliverables directly to the client.",
        ], styles),
        entry("<b>Virtual School</b>, Technology Intern", "Jun 2024 - Aug 2024", [
            "Streamlined the applicant-review process using Google App Script and web-based tools.",
            "Completed 160+ hours of work supporting the process.",
        ], styles),
        entry("<b>Future Flyers (nonprofit)</b>, Assistant Track Coach", "Mar 2024 - Aug 2024", [
            "Organized practices alongside coaching staff and supported student-athletes at track meets.",
            "Logged 50+ volunteer hours.",
        ], styles),
        *section("LEADERSHIP AND ACTIVITIES", styles),
        entry("<b>Government Club</b>, Founder and President", "", [
            "Founded and led the student Government Club.",
        ], styles),
        entry("<b>Computer Club</b>, Officer", "", [
            "Led sessions teaching data-science fundamentals using Jupyter Notebook, MATLAB, and Excel to high school students.",
        ], styles),
        entry("<b>NASA Virginia Earth and Science Scholar</b>", "", [
            "Selected as a NASA Virginia Earth and Science Scholar.",
        ], styles),
        entry("<b>Computer Science Honor Society and Technology Student Association</b>, Member", "", [
            "Competed in data science, web development, and geospatial technology events from 2021 - 2024.",
        ], styles),
        *section("SKILLS", styles),
        p("Programming and query languages: Python, SQL, JavaScript, Java, HTML/CSS", styles["skills"]),
        p("Tools and platforms: ArcGIS, MATLAB, Jupyter Notebook, Google App Script, Microsoft Excel", styles["skills"]),
        p("Core competencies: Geospatial data visualization, data analysis, IT project management, web development", styles["skills"]),
    ]
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
