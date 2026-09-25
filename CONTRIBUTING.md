# Contributing

Thanks for helping improve Career Application Pipeline.

This project is a file-based, agent-agnostic workflow for CV ingestion, job-search planning, verified role discovery, and draft application packs. Contributions should preserve the core principles: local-first, source-backed, draft-only, and no fabricated claims.

## Good first contributions

- Add synthetic example CVs for different career stages or sectors.
- Improve templates for CV feedback, cover letters, source inventories, or application packs.
- Add sample prompts for specific agents without making the repo depend on that agent.
- Improve JSON schemas and validation scripts.
- Add documentation for ATS/job-source patterns.
- Add privacy, safety, or provenance checks.

## Contribution rules

1. **Do not include real private CVs, personal data, access tokens, or recruiter contact data.** Use synthetic examples.
2. **Keep it agent agnostic.** It is fine to add examples for Claude, Codex, Cursor, ChatGPT, OpenHands, Goose, etc., but the core workflow must not depend on one vendor.
3. **Keep paths portable.** Use user-provided workspace paths or relative examples. Avoid hardcoded home directories.
4. **Do not encourage automated submissions or outreach without approval.** Drafting is fine; external action needs explicit user approval.
5. **Prefer source-backed workflows.** Job recommendations should include direct source URLs and provenance notes.

## Local validation

Run:

```bash
python3 scripts/init_workspace.py --workspace ./demo-workspace --force
python3 scripts/validate_workspace.py ./demo-workspace
python3 -m json.tool schemas/candidate-profile.schema.json >/dev/null
python3 -m json.tool schemas/job.schema.json >/dev/null
python3 -m json.tool schemas/search-criteria.schema.json >/dev/null
python3 -m json.tool schemas/source-inventory.schema.json >/dev/null
python3 -m json.tool schemas/workspace-config.schema.json >/dev/null
```

## Pull request checklist

- [ ] No real private candidate data or secrets.
- [ ] No vendor lock-in introduced to the core playbook.
- [ ] Workspace paths remain portable.
- [ ] Templates remain draft-only and approval-gated.
- [ ] Validation commands pass.
- [ ] README/docs updated if user-facing behavior changed.
