# Career Application Pipeline

> A local-first, agent-agnostic workflow that turns a CV/resume into a structured job-search system and draft application-pack pipeline.

[![Validate](https://github.com/RichardAtCT/career-application-pipeline/actions/workflows/validate.yml/badge.svg)](https://github.com/RichardAtCT/career-application-pipeline/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Agent agnostic](https://img.shields.io/badge/agent-agnostic-blue)
![Local first](https://img.shields.io/badge/local--first-privacy-green)

Most AI job-search help stops at a one-shot resume rewrite or a generic cover letter. This repo gives any capable AI/coding agent a **durable workflow**: ingest a CV, build a structured profile, infer search tracks, verify real roles, score fit, maintain a tracker, and create reviewable application packs.

It is deliberately **not tied to any specific agent runtime**. Use it with Claude Code, Codex, Cursor, ChatGPT, OpenHands, Goose, local LLM agents, or a human assistant following the files.

## Who this is for

- **Job seekers** who want targeted, evidence-backed applications rather than AI-generated spray-and-pray.
- **Career coaches** who want a repeatable client workflow with clear artifacts.
- **AI-agent builders** who want a practical file-based workflow/benchmark for research, writing, browsing, and provenance.
- **Developers** experimenting with local-first personal automation.

## What it does

| Stage | Output |
|---|---|
| CV ingestion | Extracted CV text, parse notes, explicit unknowns |
| Candidate profile | `cv/parsed-profile.yaml` with grounded facts only |
| CV improvement | `cv/cv-feedback.md` with edits, gaps, and rewrite suggestions |
| Cover-letter style | Example letter and reusable style guidance |
| Search strategy | Search tracks, criteria, source inventory, scoring weights |
| Role discovery | Verified roles, deduped tracker rows, score breakdowns |
| Application packs | Tailored CV, cover letter, fit memo, company brief, form answers, provenance |
| Automation | Optional strong-match monitor and weekly digest prompts |

## Quick start

```bash
git clone https://github.com/RichardAtCT/career-application-pipeline.git
cd career-application-pipeline
python3 scripts/init_workspace.py --workspace ./demo-workspace
python3 scripts/validate_workspace.py ./demo-workspace
```

Then point your preferred agent at this repo and your CV.

To create an application record from a verified posting (with duplicate protection), use:

```bash
python3 scripts/create_application_record.py --workspace ./demo-workspace \
  --company "Example Labs" --role "Data Intern" --location "Remote, USA" \
  --source-url "https://careers.example.com/jobs/123" --remote-policy remote
```

Use `--show-status` to list the controlled status for each tracker record. This local helper never opens an employer site, creates accounts, uploads documents, or submits applications.

### Copy-paste agent prompt

```text
Use the Career Application Pipeline in this repository.

Workspace: ./my-job-search
CV source: ./my-cv.pdf

Follow AGENT_PLAYBOOK.md. Run staged onboarding:
1. ingest my CV locally where possible;
2. create a structured candidate profile with unknowns explicit;
3. suggest CV edits and missing metrics;
4. produce an example cover-letter style;
5. infer search tracks and ask only material clarifying questions;
6. create the tracker and source inventory;
7. run one manual, source-backed search before proposing automation.

Safety: do not upload my CV, send outreach, submit applications, or invent facts without explicit approval.
```

## Demo: what a workspace looks like

After initialization, the agent works inside a portable workspace like this:

```text
job-search-workspace/
├── config.yaml
├── cv/
│   ├── original/
│   ├── parsed-profile.yaml
│   ├── search-criteria.yaml
│   ├── cv-feedback.md
│   └── example-cover-letter.md
├── tracker.csv
├── source-inventory.yaml
├── roles/
│   ├── raw/
│   ├── staged/
│   └── verified/
├── applications/
│   └── YYYY-MM-DD_company_role/
│       ├── job.yaml
│       ├── application-log.md
│       ├── 01_role/job-description.md
│       ├── 02_background/role-fit-memo.md
│       ├── 03_application-materials/cover-letter.md
│       └── 05_provenance/scoring-breakdown.yaml
├── templates/
└── logs/
```

Try the synthetic example CV:

```bash
python3 scripts/init_workspace.py --workspace ./demo-workspace --force
```

Then ask your agent:

```text
Use examples/sample-cv.md as the CV source and demo the onboarding workflow in ./demo-workspace. Do not search the live web yet; just create the profile, feedback, cover-letter example, and search criteria.
```

## Repository map

```text
.
├── AGENT_PLAYBOOK.md                 # Main operating instructions for any AI/coding agent
├── WORKFLOW.md                       # Human-readable end-to-end process
├── docs/
│   ├── privacy-and-safety.md         # Safety defaults and data handling rules
│   ├── agent-integration.md          # How to use this with different agents
│   └── automation.md                 # Portable monitor/digest patterns
├── examples/
│   └── sample-cv.md                  # Synthetic CV for testing the setup flow
├── schemas/                          # JSON schemas for key workspace files
├── scripts/
│   ├── init_workspace.py             # Dependency-free workspace initializer
│   ├── validate_workspace.py         # Lightweight sanity checks
│   └── create_application_record.py  # Creates and deduplicates application-pack records
└── templates/                        # Workspace and application-pack templates
```

## Core principles

- **Agent agnostic:** works with any assistant that can read files, write files, and optionally browse/search.
- **Local first:** parse and store CV/profile data locally where possible.
- **Source backed:** every recommended role needs a source URL and verification note.
- **Draft only:** never submit applications or send outreach without explicit approval.
- **No fabrication:** unknown salary, work authorization, dates, contacts, or metrics stay `unknown`.
- **Reviewable artifacts:** every application pack contains provenance and caveats.
- **Human in control:** the agent prepares materials; the user approves claims, submissions, and outreach.

## Why file-based?

A job search is stateful. A durable workspace lets an agent:

- preserve corrections and preferences across sessions;
- avoid re-parsing the CV every time;
- dedupe roles and preserve application status;
- create auditable application materials;
- maintain a controlled application status and per-role event log;
- run safely with different agent runtimes or schedulers.

## Suggested GitHub topics

`ai-agents`, `job-search`, `resume`, `career`, `cover-letter`, `workflow`, `agentic-ai`, `templates`, `automation`, `ats`, `local-first`

## Contributing

Contributions are welcome. Good first contributions include:

- additional synthetic example CVs;
- improved schemas;
- ATS/source inventory adapters;
- application-pack templates;
- sample prompts for different agents;
- privacy/safety improvements.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`ROADMAP.md`](ROADMAP.md).

## License

MIT. See [`LICENSE`](LICENSE).
