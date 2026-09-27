# Conversational Job-Search Interface

Use ordinary requests; you do not need to know file paths, scripts, or schemas. Codex maps the request to the existing workspace workflow and keeps records locally.

## Find roles

Say: “Find Summer 2027 internships that fit me,” or “Search Handshake too.”

Codex uses the candidate profile and search criteria, searches configured sources, verifies promising listings at direct employer pages, removes duplicates, and adds suitable roles to the tracker. It reports only source-backed jobs and does not apply.

## Prepare an application

Say: “Prepare the Peraton software engineering internship,” or paste a job URL or description.

Codex verifies the posting, checks for duplicates, prepares a truthful job summary, fit memo, tailored CV draft, answers, and readiness report. It asks for missing facts instead of guessing.

## Start an application

Say: “Start the ICF application and fill the allowed fields.”

This requires explicit approval for that exact company and role. Codex can use the prepared pack and fill only authorized GREEN and YELLOW fields. It stops for RED or unknown fields, including passwords, codes, CAPTCHAs, attestations, demographic disclosures, background checks, and final submission. Account creation and resume uploads each require their own explicit approval.

## Check application status

Say: “What needs my attention?”, “Show active applications,” “Which companies have not responded?”, “Show applications at the interview stage,” or “How many internships did I submit this month?”

Codex summarizes the local tracker and application records, prioritizing roles that need an action. It does not claim a role was submitted unless the user confirmed submission.

## Record employer email

Say: “Record this interview email for Peraton,” or, after explicit read-only Gmail authorization, “Check my job-search Gmail for updates.”

Codex records minimal message metadata, classifies it, and asks for confirmation before changing status. It never sends a reply automatically; it may prepare a draft for review.

## Update preferences or facts

Say: “I can work until August 15,” “I have a driver's license,” or “Do not show me defense jobs.”

Codex distinguishes candidate facts from job-search preferences, updates the appropriate canonical record, and leaves unrelated data unchanged.

## Always user-controlled

Codex never invents qualifications, stores secrets, bypasses security checks, sends outreach, or makes final submissions. The user handles passwords, MFA, verification codes, CAPTCHAs, legal attestations, sensitive disclosures, and final submission.
