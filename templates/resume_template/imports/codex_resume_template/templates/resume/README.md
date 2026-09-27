# Locked Tailored-Resume Template

This folder contains the only approved visual template for job-specific resumes.

## Files

- `resume_template.tex` — editable LaTeX source. Formatting is treated as locked.
- `resume_reference.png` — visual reference for the intended appearance.
- `RESUME_RULES.md` — instructions Codex must follow when tailoring resumes.

## Codex usage

For every target job:

1. Read the job description.
2. Read the verified candidate profile and master resume.
3. Copy `resume_template.tex` into the target application's folder. Never edit the master template for an individual application.
4. Change candidate content only: entries, bullets, section inclusion, ordering where permitted, and verified skills.
5. Do not change document class, margins, fonts, heading styling, rules, indentation, spacing, or overall visual structure merely to fit more content.
6. Compile the copied `.tex` file to PDF.
7. Verify that the PDF is one page and visually renders correctly.
8. If it is longer than one page, shorten/remove the least relevant content first. Do not shrink the template to force content onto one page.
9. Save both the tailored `.tex` source and PDF in the application folder.
10. Never overwrite the master resume or this template.

## Suggested application output

```text
applications/
  company-name/
    role-name/
      job_description.md
      fit_analysis.md
      resume.tex
      First_Last_Resume.pdf
      application_answers.md
      application_log.md
```

## Compile

With a TeX distribution installed:

```bash
pdflatex -interaction=nonstopmode -halt-on-error resume.tex
```

Run it a second time if hyperlink metadata or references require it.
