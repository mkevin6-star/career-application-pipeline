# Agent Integration

This project is agent agnostic. Use it with any assistant that can read/write files and optionally browse/search the web.

## Recommended prompt

```text
Use this repository's AGENT_PLAYBOOK.md as your operating instructions.
Workspace: <path>
CV source: <path or pasted text>

Run the staged onboarding flow. Keep all generated artifacts in the workspace. Do not submit applications or send outreach without explicit approval.
```

## Natural-language operation

For common requests such as finding roles, preparing an application, starting an approved application, checking status, or recording employer email, see [`conversational-interface.md`](conversational-interface.md). The user should not need to invoke local scripts directly; scripts provide durable local state and validation behind the agent workflow.

## Runtime requirements

Minimum:

- file read/write;
- ability to parse text from the supplied CV format;
- ability to write YAML/CSV/Markdown.

For full search:

- web search or browser access;
- ability to fetch direct job pages;
- optional scheduler/cron for recurring monitoring.

## Adapting paths

Never assume a particular home directory. Use the workspace path supplied by the user. If no path is supplied, create `job-search-workspace` under the current working directory.
