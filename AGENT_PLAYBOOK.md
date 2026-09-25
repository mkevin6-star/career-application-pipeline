# Agent Playbook: Career Application Pipeline

This is the main instruction file for any AI agent using this repository.

You are setting up a user's job-search and application-pack workflow from their CV/resume. Your output must be grounded in the user's supplied CV, their corrections, and source-backed job postings. Do not invent facts.

## Non-negotiable rules

1. **Do not submit applications, send emails, send LinkedIn messages, upload CVs, or contact anyone without explicit approval.**
2. **Do not fabricate candidate achievements, metrics, qualifications, work authorization, salary expectations, references, contacts, or job availability.**
3. **Every recommended job must include a source URL.** Prefer direct employer/ATS URLs over aggregator snippets.
4. **Mark unknowns explicitly** as `unknown` or `needs_user_input`.
5. **Use staged onboarding.** Do not ask a giant questionnaire upfront. Infer from the CV, then ask only material questions.
6. **Keep private data local** unless the user approves a third-party service.
7. **Separate facts from suggestions.** CV edits and cover letters may improve wording but must not add unverified claims.

## Application field and browser rules

For application filling, load `application-field-rules.md` from the workspace before entering any employer form. `cv/parsed-profile.yaml` is the source of candidate facts and `cv/search-criteria.yaml` is the source of job-search preferences.

- **GREEN** fields may be entered only after the user explicitly approves work for that employer and the exact value is verified in the canonical profile.
- **YELLOW** fields require an exact stored answer; if one is missing or ambiguous, stop and ask the user.
- **RED** fields are always user-handled: passwords, MFA and verification codes, CAPTCHAs, IDs, banking data, signatures, attestations, voluntary demographic disclosures, criminal-history questions, background-check authorizations, and unclear questions.
- Creating an applicant account requires immediate user confirmation. Resume uploads require explicit approval for that employer. The user performs final submission and the tracker changes to `applied` only after the user confirms it.

## Default onboarding sequence

### Step 1 — Create or load workspace

Use the user-provided workspace path. If none is provided, ask for one or use a local directory named `job-search-workspace` in the current project/session directory.

Required files:

- `config.yaml`
- `cv/parsed-profile.yaml`
- `cv/search-criteria.yaml`
- `cv/cv-feedback.md`
- `tracker.csv`
- `source-inventory.yaml`
- `applications/`
- `roles/raw/`, `roles/staged/`, `roles/verified/`

If the repo's `scripts/init_workspace.py` is available, use it.

### Step 2 — Ingest CV

Extract the CV text locally where possible. Save original files under `cv/original/` when allowed, extracted text under `cv/original/extracted-cv.txt`, and parsing caveats under `cv/parse-notes.md`.

### Step 3 — Build structured candidate profile

Write `cv/parsed-profile.yaml` using `schemas/candidate-profile.schema.json` as the contract.

Use this shape:

```yaml
candidate:
  name: unknown
  location: unknown
  current_title: unknown
  current_company: unknown
  years_experience: unknown
  seniority_level: unknown
  industries: []
  functions: []
  domains: []
  hard_skills: []
  soft_skills: []
  leadership_scope: []
  notable_achievements: []
  education: []
  certifications: []
  languages: []
  work_authorization: unknown
  constraints: []
  dealbreakers: []
  unknowns: []
```

Do not include unsupported claims.

### Step 4 — Review profile with the user

Present a concise review:

- strongest positioning;
- likely role families;
- missing information that materially affects search;
- ambiguous claims or gaps;
- potential ATS keyword gaps;
- proposed edits to the CV.

Ask only questions that materially change the search, usually: geography/time zones, remote policy, role families, compensation/seniority floor, industries/employers to exclude, and work authorization constraints.

### Step 5 — Produce CV feedback

Write `cv/cv-feedback.md` with a positioning summary, issue table, bullet rewrites, missing metrics/questions, and a suggested one-page CV structure.

### Step 6 — Establish cover-letter style

If the user provided a sample, derive style guidance from it. Otherwise choose or ask about one of: `concise-direct`, `warm-narrative`, `executive-strategic`, `sector-specific`.

Write `cv/example-cover-letter.md` as a sample for a plausible target role. Label it clearly as an example, not a final application letter.

### Step 7 — Infer search tracks

Write `cv/search-criteria.yaml` using `schemas/search-criteria.schema.json`. Create separate tracks when the CV supports distinct directions, e.g. product leadership, data science, operations, philanthropy, fractional advisory, or startup roles.

Each track should include target titles, adjacent titles, excluded titles, keywords, target industries, target company types, geography/remote policy, seniority, scoring adjustments, and outreach angles.

### Step 8 — Create source inventory

Write `source-inventory.yaml` with sources grouped by direct employers, ATS platforms, job boards, niche boards, portfolio boards, search backfill, recruiter sources, and social/search sources.

### Step 9 — Run first manual search

Before automation, run one manual search to validate the criteria:

1. Search configured sources and queries.
2. Stage raw hits in `roles/raw/`.
3. Verify promising roles from direct source/job pages.
4. Deduplicate by canonical URL and normalized company/title.
5. Score with the rubric below.
6. Append/update `tracker.csv`.
7. Report only verified roles worth attention.

### Step 10 — Score roles

Default score out of 100:

| Category | Points |
|---|---:|
| Role/function fit | 25 |
| Seniority and leadership scope fit | 15 |
| Industry/domain fit | 15 |
| Geography/remote/travel fit | 15 |
| Skills and keyword match | 10 |
| Company quality/signal | 10 |
| Compensation likelihood | 5 |
| Freshness/timing/application path | 5 |

Decision bands: `85-100` priority, `75-84` strong, `60-74` possible, `<60` skip/archive unless broad coverage was requested.

### Step 11 — Build application packs

For strong matches or user-selected roles, create:

```text
applications/YYYY-MM-DD_company-slug_role-slug/
├── job.yaml
├── application-log.md
├── 00_README.md
├── 01_role/job-description.md
├── 01_role/source-url.txt
├── 01_role/application-url.txt
├── 02_background/company-brief.md
├── 02_background/role-fit-memo.md
├── 02_background/concerns-and-risks.md
├── 02_background/contact-research.md
├── 03_application-materials/tailored-cv.md
├── 03_application-materials/tailored-cv.pdf
├── 03_application-materials/cover-letter.md
├── 03_application-materials/cover-letter.pdf
├── 04_application-form/suggested-answers.md
├── 04_application-form/salary-location-notes.md
├── 04_application-form/documents-checklist.md
└── 05_provenance/
```

Application packs are draft-only unless the user explicitly approves submission/outreach.

Keep each tracker status within this controlled set: `discovered`, `saved`, `preparing`, `ready_for_application`, `ready_for_review`, `applied`, `assessment`, `interview`, `offer`, `rejected`, `withdrawn`, `skipped`, or `archived`. Record material milestones in `application-log.md` without secrets. Before creating a pack, check the tracker for the same canonical source URL, application URL, job ID, or normalized company/title/location and show a probable duplicate instead of creating another record.

### Step 12 — Offer automation

Only after the first manual search works, propose a strong-match monitor and weekly digest using the user's preferred scheduler or agent runtime. Do not create scheduled jobs without user approval.

## Verification checklist before declaring setup complete

- [ ] CV text extracted or pasted text captured.
- [ ] Candidate profile written with unknowns explicit.
- [ ] Search criteria written and reviewed.
- [ ] CV feedback written.
- [ ] Example cover letter written.
- [ ] Tracker exists with correct headers.
- [ ] Source inventory exists.
- [ ] At least one manual search has been run or the blocker is documented.
- [ ] Recommended roles have source URLs.
- [ ] No external application/outreach action was taken without approval.
