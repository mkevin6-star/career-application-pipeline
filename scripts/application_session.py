#!/usr/bin/env python3
"""Record optional browser-application milestones without browser automation.

This local helper never opens a browser, creates an external account, uploads a
document, enters a form, or submits an application. An agent may use the
resulting audit record only after the user has explicitly approved that exact
employer activity.
"""
from __future__ import annotations

import argparse
import csv
import re
from datetime import date
from pathlib import Path

TRACKER_HEADERS = [
    "role_id", "date_seen", "last_seen", "company", "role_title", "location", "remote_policy",
    "source_url", "application_url", "score", "status", "next_action", "follow_up_date",
    "application_pack_path", "notes",
]


def read_tracker(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_tracker(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=TRACKER_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def replace_yaml_value(text: str, key: str, value: str, indent: str = "") -> str:
    pattern = rf"^{re.escape(indent)}{re.escape(key)}:.*$"
    replacement = f"{indent}{key}: {value}"
    updated, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"expected exactly one {indent}{key} field in job.yaml")
    return updated


def append_log(path: Path, message: str) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(f"\n{date.today()} — {message}\n")


def write_session(path: Path, action: str, reference: str) -> None:
    text = path.read_text(encoding="utf-8")
    if action == "start":
        text = text.replace("- Employer-specific approval: not_recorded", f"- Employer-specific approval: {reference}")
    elif action == "ready-for-review":
        text = text.replace("- Employer-specific approval: not_recorded", f"- Employer-specific approval: {reference}")
        text = text.replace("- Fields left for user: not_recorded", "- Fields left for user: RED fields and final submission")
    elif action == "submitted":
        text = text.replace("- Final submission: user action only", f"- Final submission: user confirmed ({reference})")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Record safe browser-session milestones locally.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--role-id", required=True)
    parser.add_argument("--action", required=True, choices=["start", "ready-for-review", "submitted"])
    parser.add_argument("--approval-reference", help="Required for start and ready-for-review; records the user's employer-specific approval.")
    parser.add_argument("--user-confirmation", help="Required for submitted; records the user's confirmation that they submitted.")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    tracker_path = workspace / "tracker.csv"
    rows = read_tracker(tracker_path)
    matching = [row for row in rows if row["role_id"] == args.role_id]
    if len(matching) != 1:
        parser.error(f"expected exactly one tracker record for {args.role_id}")
    row = matching[0]
    pack = workspace / row["application_pack_path"]
    job_file = pack / "job.yaml"
    session_file = pack / "04_application-form" / "browser-session.md"
    if not job_file.exists() or not session_file.exists():
        parser.error("application pack is incomplete; materialize and prepare it before recording a browser session")

    if args.action in {"start", "ready-for-review"} and not args.approval_reference:
        parser.error(f"{args.action} requires --approval-reference after explicit user approval for this employer")
    if args.action == "submitted" and not args.user_confirmation:
        parser.error("submitted requires --user-confirmation after the user personally submits the application")

    job_text = job_file.read_text(encoding="utf-8")
    if args.action == "start":
        job_text = replace_yaml_value(job_text, "browser_started", "true", "  ")
        write_session(session_file, args.action, args.approval_reference)
        append_log(pack / "application-log.md", f"Browser session authorized for this employer: {args.approval_reference}. No submission recorded.")
    elif args.action == "ready-for-review":
        job_text = replace_yaml_value(job_text, "status", "ready_for_review")
        job_text = replace_yaml_value(job_text, "ready_for_review", "true", "  ")
        job_text = replace_yaml_value(job_text, "submitted", "false", "  ")
        row["status"] = "ready_for_review"
        row["next_action"] = "User review and submission"
        write_session(session_file, args.action, args.approval_reference)
        append_log(pack / "application-log.md", f"Application marked ready for user review: {args.approval_reference}. Final submission remains user-only.")
    else:
        job_text = replace_yaml_value(job_text, "status", "applied")
        job_text = replace_yaml_value(job_text, "submitted", "true", "  ")
        job_text = replace_yaml_value(job_text, "applied", str(date.today()), "  ")
        row["status"] = "applied"
        row["next_action"] = "Await employer response"
        write_session(session_file, args.action, args.user_confirmation)
        append_log(pack / "application-log.md", f"User confirmed final submission: {args.user_confirmation}.")

    job_file.write_text(job_text, encoding="utf-8")
    write_tracker(tracker_path, rows)
    print(f"Recorded {args.action} for {args.role_id}. No browser or external action was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
