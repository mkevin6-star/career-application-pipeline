# Codex Job Search System — Implementation Plan

## Goal

Turn the existing Career Application Pipeline repository into a personal job-search operating system that Codex can maintain and extend.

The system should:

- Use verified candidate information as the source of truth.
- Prepare job-specific resumes and application materials.
- Track every discovered and submitted job.
- Support browser-assisted application filling when browser capabilities are available.
- Use a dedicated Gmail account owned by the user for job applications.
- Automatically fill routine, verified application fields.
- Stop and ask the user when an answer is unknown, sensitive, ambiguous, or requires user action.
- Never invent candidate information.
- Never submit a final application without the user reviewing and submitting it.

Codex should implement this plan incrementally. Preserve useful existing repository functionality unless a change is necessary.

---

# Phase 1 — Build the Candidate Profile and Rules System

## Objective

Create one reliable source of truth for everything Codex is allowed to use when preparing or filling applications.

## Tasks

### 1. Create the profile structure

Create this structure if equivalent files do not already exist:

```text
profile/
├── candidate.yaml
├── preferences.yaml
├── application_rules.md
├── master_resume.md
├── master_resume.pdf
└── answers/
    ├── common.md
    └── manual_only.md
```

Reuse existing repository files when appropriate instead of creating duplicates.

### 2. Create `candidate.yaml`

Store verified facts only.

Recommended structure:

```yaml
identity:
  first_name: ""
  middle_name: ""
  last_name: ""

contact:
  email: ""
  phone: ""
  city: ""
  state: ""
  country: "United States"

education:
  school: ""
  degree: ""
  major: ""
  graduation_date: ""

links:
  linkedin: ""
  github: ""
  portfolio: ""

work_authorization:
  authorized_to_work_in_us: null
  sponsorship_required: null
```

Do not guess missing values. Leave them blank/null and ask the user when needed.

### 3. Create `preferences.yaml`

Store job-search preferences separately from candidate facts.

Include fields such as:

```yaml
roles: []
locations: []
remote_preference: ""
employment_types:
  - internship
industries: []
excluded_companies: []
minimum_salary: null
relocation: null
```

### 4. Create application field rules

In `application_rules.md`, define three categories.

#### GREEN — May fill automatically

Examples:

- First and last name
- Verified email address
- Verified phone number
- City/state
- University
- Degree
- Major
- Graduation date
- LinkedIn
- GitHub
- Portfolio
- Resume upload

Only fill a GREEN field when the value exists in the source-of-truth files.

#### YELLOW — Fill only when an explicit stored answer exists

Examples:

- Desired salary
- Relocation
- Start date
- Travel willingness
- Work authorization
- Sponsorship
- Previous employment with the company
- Referral source

If an exact answer does not exist, stop and ask the user.

#### RED — User handles manually

Examples:

- SSN
- Passport/government ID numbers
- Bank/payment information
- Passwords
- MFA and verification codes
- CAPTCHAs
- Electronic signatures or attestations
- Voluntary demographic/EEO/disability/veteran disclosures
- Criminal-history questions
- Background-check authorizations
- Any field whose meaning is unclear

### 5. Add permanent rules to `AGENTS.md`

Add instructions stating:

1. The user is always the applicant.
2. Candidate facts must come from the profile, resume, or information explicitly provided by the user.
3. Never invent, infer, exaggerate, or embellish experience or qualifications.
4. Never store passwords, MFA secrets, recovery codes, SSNs, banking information, or government ID numbers in the repository.
5. If a required answer is unknown, ask the user.
6. Final application submission must remain a user action.
7. Browser security mechanisms must not be bypassed.

## Completion Criteria

Phase 1 is complete when Codex can answer:

- What information may I automatically use?
- What information requires an explicit stored answer?
- What must the user handle manually?
- What roles is the user searching for?
- Which candidate facts are still missing?

---

# Phase 2 — Build the Job and Application Workspace

## Objective

Give every job a permanent record so Codex can prepare applications consistently and avoid duplicates.

## Tasks

### 1. Create the application structure

Use a structure similar to:

```text
applications/
└── COMPANY/
    └── ROLE/
        ├── job.yaml
        ├── job_description.md
        ├── fit_analysis.md
        ├── answers.yaml
        ├── application_log.md
        └── materials/
            ├── resume.md
            ├── resume.pdf
            └── cover_letter.md
```

### 2. Define `job.yaml`

Recommended fields:

```yaml
company: ""
role: ""
location: ""
job_id: ""
job_url: ""
application_url: ""

status: "discovered"

dates:
  discovered: ""
  prepared: null
  applied: null

account:
  created: false
  email: ""

application:
  resume_version: ""
  browser_started: false
  ready_for_review: false
  submitted: false
```

### 3. Define statuses

Use a controlled set such as:

```text
discovered
saved
preparing
ready_for_application
ready_for_review
applied
assessment
interview
offer
rejected
withdrawn
skipped
```

### 4. Implement duplicate protection

Before creating a new application, check existing records using as many of these as available:

- Company
- Job ID
- Job URL
- Application URL
- Role
- Location

If a probable duplicate exists, stop and show the existing application instead of creating another one.

### 5. Create an application log

Record important events without secrets.

Example:

```text
2026-09-25 — Job discovered
2026-09-25 — Resume prepared
2026-09-26 — Application opened
2026-09-26 — Ready for user review
2026-09-26 — User confirmed application was submitted
```

## Completion Criteria

Phase 2 is complete when Codex can create a job workspace from a posting, detect duplicates, show its current status, and maintain an auditable application history.

---

# Phase 3 — Build the Application Preparation Pipeline

## Objective

Turn a job posting into a complete application package before browser automation begins.

## Tasks

### 1. Create a single preparation workflow

The command/concept should be:

```text
Prepare application for <job URL or job description>
```

The workflow should:

1. Read the job description.
2. Extract company, title, location, requirements, preferred qualifications, responsibilities, and application URL.
3. Run duplicate detection.
4. Create the application workspace.
5. Compare requirements against the candidate profile and master resume.
6. Save `fit_analysis.md`.
7. Create a tailored resume using only truthful existing experience.
8. Prepare job-specific answers where enough verified information exists.
9. Create a cover letter only when requested or useful.
10. Mark the application `ready_for_application`.

### 2. Define resume tailoring rules

Codex may:

- Reorder existing experience.
- Emphasize relevant skills.
- Rewrite bullets for clarity.
- Select the most relevant projects.
- Adjust summaries/objectives.
- Use terminology from the job posting when truthful.

Codex may not:

- Invent skills.
- Invent metrics.
- Invent employment.
- Invent projects.
- Change dates to improve appearance.
- Claim experience that cannot be supported by the source profile/resume.

### 3. Build reusable answer material

Use `profile/answers/common.md` for verified reusable material such as:

- Technical interests
- Career interests
- Project summaries
- Programming experience
- Leadership examples
- Teamwork examples

Codex may tailor wording to a particular employer but must preserve the underlying facts.

### 4. Add a preparation report

At the end of preparation, report:

```text
APPLICATION PREPARED

Company:
Role:
Location:

Resume: Ready
Cover letter: Ready / Not required
Application answers: Ready / Some user input required
Duplicate check: Passed

Next step: Start application
```

## Completion Criteria

Phase 3 is complete when a single Codex request can turn a posting into an organized, truthful, job-specific application package.

---

# Phase 4 — Add Browser-Assisted Application Filling

## Objective

Allow the workflow to fill routine application fields when Codex is running in an environment with browser/computer-use capabilities.

Browser functionality must be treated as optional. The repository should still work when no browser capability is available.

## Workflow

The user should be able to request:

```text
Start the application for <company/role>
```

Then execute:

```text
Open application
      ↓
Check application record
      ↓
Create/login to applicant account if needed
      ↓
User handles password/MFA/CAPTCHA when required
      ↓
Upload prepared resume
      ↓
Fill GREEN fields
      ↓
Fill YELLOW fields with stored answers
      ↓
Unknown/RED question?
   YES        NO
    ↓          ↓
Ask user    Continue
    └──────┬───┘
           ↓
      Final review
           ↓
          STOP
           ↓
      User reviews
           ↓
      User submits
```

## Applicant Accounts

Use the user's dedicated job-search email when an employer requires an applicant account.

Codex may fill verified identity/contact information for account creation when allowed by `application_rules.md`.

The user handles:

- Password creation/entry when needed
- MFA
- Email/phone verification codes
- CAPTCHAs
- Security challenges

Never save these secrets in Git.

## Unknown Questions

When Codex encounters an unanswered question:

1. Identify the exact field/question.
2. Determine whether it is GREEN, YELLOW, or RED.
3. Search the verified profile and reusable answers.
4. If no authorized answer exists, stop.
5. Ask the user for the answer.
6. Ask whether the answer should be stored for future applications when appropriate.
7. Continue after receiving the answer.

## Final Review

Before submission, Codex should provide a concise summary containing:

- Company
- Position
- Resume used
- Contact information entered
- Important application answers
- Fields left for the user
- Any warnings or uncertainty

Set:

```yaml
ready_for_review: true
submitted: false
```

Do not change `submitted` to `true` until the user confirms they actually submitted the application.

## Completion Criteria

Phase 4 is complete when routine application forms can be filled consistently from verified data while unknown, sensitive, security-related, and final-submission actions reliably return control to the user.

---

# Phase 5 — Add Persistent Tracking and Gmail Workflow

## Objective

Turn the repository from an application generator into a system that tracks the full job-search lifecycle.

## Tasks

### 1. Add SQLite

Create a database such as:

```text
data/jobs.db
```

Recommended tables:

```text
jobs
applications
companies
application_answers
resume_versions
events
```

Filesystem application folders remain the source for human-readable documents. SQLite provides fast structured tracking.

### 2. Synchronize status

Application folder status and database status should remain consistent.

Do not silently overwrite conflicting information. Log changes.

### 3. Support useful Codex queries

The system should eventually answer requests such as:

```text
Show my active applications.

Which applications need action?

Which companies haven't responded?

Show saved jobs I haven't applied to.

How many internships did I apply to this month?

Show all applications currently at the interview stage.
```

### 4. Integrate the dedicated Gmail workflow

When authorized Gmail access is available, use the dedicated job-search inbox to associate employer messages with applications.

Classify relevant messages into categories such as:

```text
application_received
assessment
action_required
interview
recruiter_outreach
rejection
offer
other
```

### 5. Update application records from email carefully

Examples:

- Confirmation email → record application confirmation.
- Assessment invitation → status may become `assessment`.
- Interview scheduling message → status may become `interview`.
- Rejection → status may become `rejected`.

Preserve the supporting email reference in the event history when possible.

Do not automatically send recruiter responses in the initial implementation. Prepare a draft/recommended response for user review instead.

## Completion Criteria

Phase 5 is complete when Codex can show the state of the job search from persistent application data and, when Gmail is connected, recognize important employer updates without requiring the user to manually update every record.

---

# Phase 6 — Create the Conversational Job-Search Interface

## Objective

Hide the internal complexity so the user can operate the entire system through simple Codex requests.

## Required Commands / Intents

Codex should understand requests similar to:

### Discover

```text
Find internships that fit me.
```

Use `preferences.yaml` and the candidate profile. Save useful jobs rather than losing them after the session.

### Prepare

```text
Prepare the Capital One software engineering internship.
```

Run the Phase 3 preparation pipeline.

### Apply

```text
Start the Capital One application.
```

Run the Phase 4 browser workflow when browser capabilities are available.

### Status

```text
What's happening with my applications?
```

Summarize applications that need attention first, followed by other active applications.

### Follow-up

```text
Show companies that haven't responded.
```

Use the application database and authorized Gmail data when available.

## Automation Boundaries

The final system should optimize repetitive work while preserving these boundaries:

### Codex can do automatically

- Organize job records.
- Analyze job descriptions.
- Tailor resumes truthfully.
- Prepare application answers from verified information.
- Detect duplicates.
- Track statuses.
- Fill routine application fields when browser capabilities exist.
- Upload prepared application materials.
- Categorize employer emails when Gmail access is authorized.
- Prepare suggested recruiter responses.

### Codex should return control to the user for

- Unknown candidate facts.
- Sensitive information.
- Passwords and authentication secrets.
- MFA/verification codes.
- CAPTCHAs/security challenges.
- Ambiguous legal or attestation questions.
- Final application review and submission.

## Final Architecture

```text
                         CODEX
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
    CANDIDATE          JOB SEARCH        GMAIL
     PROFILE              DATA            INBOX
          │                │                │
          └────────────┬───┴────────────────┘
                       ↓
                APPLICATION
                  PIPELINE
                       ↓
                JOB ANALYSIS
                       ↓
               RESUME TAILORING
                       ↓
               BROWSER ASSISTANCE
                       ↓
                 FINAL REVIEW
                       ↓
                      USER
                       ↓
                    SUBMIT
                       ↓
               APPLICATION DB
```

## Completion Criteria

Phase 6 is complete when normal operation no longer requires the user to know repository paths, database schemas, or internal scripts. The user should be able to operate the system primarily through natural-language requests while Codex follows the permanent repository rules.

---

# Implementation Order for Codex

Implement the phases in this exact order:

```text
Phase 1 — Candidate Profile + Rules
              ↓
Phase 2 — Job/Application Workspace
              ↓
Phase 3 — Application Preparation
              ↓
Phase 4 — Browser Assistance
              ↓
Phase 5 — Tracking + Gmail
              ↓
Phase 6 — Conversational Interface
```

Do not attempt to build everything at once.

At the beginning of each phase:

1. Inspect the existing repository for equivalent functionality.
2. Reuse and extend existing components where reasonable.
3. Explain the planned file changes.
4. Implement the phase.
5. Add or update tests where applicable.
6. Update documentation.
7. Verify existing functionality still works.
8. Report what was completed and any user information still required.

Only then proceed to the next phase.

---

# Global Rules

These rules apply to every phase.

1. **Never fabricate applicant information.**
2. **Candidate profile and verified resume information are the source of truth.**
3. **Missing information remains missing until the user provides it.**
4. **Never commit passwords, tokens, MFA secrets, cookies, SSNs, banking information, or government ID numbers.**
5. **Use environment variables or appropriate secret storage for API credentials.**
6. **Preserve useful existing repository functionality.**
7. **Prefer modular components over one large automation script.**
8. **Keep job-search preferences separate from factual candidate information.**
9. **Keep application-specific data separate from the master candidate profile.**
10. **Maintain logs/status so another Codex session can understand previous actions.**
11. **Never bypass CAPTCHAs, MFA, security challenges, or website protections.**
12. **Stop for user input when an application question cannot be answered reliably.**
13. **Final application submission remains a user action.**
14. **Do not mark an application submitted until the user confirms submission.**
15. **Design the system so browser and Gmail integrations are optional modules rather than requirements for the core repository to function.**
