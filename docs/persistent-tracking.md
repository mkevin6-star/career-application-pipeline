# Persistent Tracking and Optional Email Intake

## Current storage decision

`tracker.csv`, each application's `job.yaml`, and its Markdown logs are the current sources of truth. This is sufficient for a small job search because the files are portable, reviewable, and the lifecycle helper can answer status questions without a database.

Do not introduce SQLite merely to duplicate these records. Re-evaluate a database only when the file-based records cannot safely answer lifecycle queries, event history becomes too large to review, or a later integration needs reliable transactional synchronization.

## Lifecycle queries

Use `scripts/application_lifecycle.py` to show all tracked roles, roles needing action, active applications awaiting an employer response, saved/prepared jobs that are not applied, a stage-specific view, or the number applied in a month.

## Optional Gmail workflow

Gmail access is disabled by default and is not required for this repository. If the user later explicitly authorizes their dedicated job-search inbox, use read-only access first and search only for messages related to tracked employers/roles. Keep only a minimal local reference: received date, category, message reference, and short subject/summary.

Allowed categories are `application_received`, `assessment`, `action_required`, `interview`, `recruiter_outreach`, `rejection`, `offer`, and `other`.

Classify a message locally with `application_lifecycle.py record-email`. The helper records an event but does not send mail, access Gmail, or change status automatically. A status transition needs explicit user confirmation; `applied` remains reserved for the user-confirmed submission path in `application_session.py`.
