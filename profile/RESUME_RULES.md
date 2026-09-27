# Resume Generation Rules

## Purpose

When creating a new resume tailored to a specific job or company, the agent MUST
use the approved resume template as the visual and structural template.

The template is FIXED.

Tailoring means changing the CONTENT to better match a job description.
Tailoring does NOT mean redesigning the resume.

---

## 0. One-Page Utilization

Every generated resume MUST use the full page effectively. It should have a
balanced, near-full one-page layout with no large unused area at the bottom.

To achieve this, the agent may select additional accurate, job-relevant
experience, projects, leadership, coursework, skills, or accomplishments from
the candidate's approved source material. The agent MUST NOT add filler,
invent claims, or change the approved template's visual design, margins,
fonts, line spacing, or section formatting merely to fill space.

---

## 0.1 File Naming

Every generated resume PDF MUST use this filename convention:

`Lastname_CompanyName.pdf`

For example, the Dewberry resume for Kevin Mathews is named
`Mathews_Dewberry.pdf`. Use the candidate's last name and the employer's name
only; do not add role names, dates, version labels, or other suffixes unless
the user explicitly asks for an exception.

---

## 1. Approved Template

Use the resume template stored at:

`templates/resume_template/`

This is the ONLY approved template for newly generated tailored resumes.

Do NOT:

- create a new resume design
- change the page layout
- use a different template
- change fonts
- change margins
- change heading styles
- change bullet formatting
- change line spacing
- change section divider formatting
- add colors
- add graphics
- add icons
- add profile photos
- add sidebars
- create multiple columns
- use a modern/graphic resume design

The final resume should visually match the approved template as closely as
possible.

---

## 2. Required Visual Structure

The resume should follow this general structure:

NAME
Contact Information

EDUCATION
------------------------------------------------

EXPERIENCE
------------------------------------------------

PROJECTS / LEADERSHIP / RELEVANT EXPERIENCE
------------------------------------------------

SKILLS
------------------------------------------------
