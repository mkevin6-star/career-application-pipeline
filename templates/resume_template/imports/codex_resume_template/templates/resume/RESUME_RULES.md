# Resume Tailoring Rules for Codex

## Non-negotiable template rule

All newly generated, company-specific resumes MUST start from `templates/resume/resume_template.tex` and preserve its visual formatting. The supplied `resume_reference.png` is the appearance reference.

Do not redesign the resume. Do not create an alternate template. Do not alter fonts, margins, section-rule styling, bullet indentation, header structure, spacing system, or page size for a particular employer unless the user explicitly requests a template change.

## Source of truth

Only use verified facts from the candidate profile, master resume, verified project/experience files, or facts explicitly supplied by the user. Never invent or infer skills, employment, projects, coursework, awards, dates, GPA, metrics, responsibilities, or accomplishments.

## Tailoring workflow

1. Parse the target job description and identify responsibilities, required qualifications, preferred qualifications, technologies, and repeated concepts.
2. Compare those requirements with verified candidate evidence.
3. Select the most relevant verified experience, projects, coursework, and skills.
4. Copy the locked template into the application's directory.
5. Rewrite bullets only to emphasize truthful aspects of existing experience. Prefer `action + work + method + result/purpose`.
6. Reorder verified skills and optional project/leadership content according to relevance.
7. Use job-description terminology only when the candidate genuinely possesses the corresponding experience or skill.
8. Compile the tailored source to PDF.
9. Check factual accuracy, spelling, alignment, clipping, bullet consistency, and one-page length.
10. If the resume exceeds one page, first remove weak bullets, shorten verbose bullets, remove less relevant entries, then compress low-value skills. Do not solve overflow by materially shrinking the locked template.
11. Store the source and PDF inside the job-specific application directory. Never overwrite the master template or master resume.

## Default section strategy

Preserve the template's overall style while selecting appropriate content. Education should remain near the top for a student/new-graduate profile. Professional Experience should contain verified employment/research experience. Projects & Leadership may prioritize technical projects for technical jobs and leadership for roles where it is more relevant. Honors and Awards is optional and should be removed when the space is more valuable for relevant experience. Skills should be concise and ordered for the target role.

## Mandatory final checks

A resume is not complete until all of the following are true:

- It uses the approved template.
- It is tailored to one specific job.
- Every factual claim is supported by verified candidate information.
- No requested qualification has been converted into a fabricated candidate skill.
- The PDF is one page unless the user explicitly allows otherwise.
- No content is clipped or overlapping.
- Dates and locations align consistently.
- The PDF opens and renders successfully.

After generation, summarize what content was emphasized, what was removed or reordered, and any important job requirements that were deliberately NOT added because supporting candidate evidence was unavailable.
