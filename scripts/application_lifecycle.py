#!/usr/bin/env python3
"""Query file-based application state and record minimal email events.

This helper is local-only. It never connects to Gmail, sends email, or changes
an application status without an explicit command from the user/agent.
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
VALID_STATUSES = {
    "discovered", "saved", "preparing", "ready_for_application", "ready_for_review",
    "applied", "assessment", "interview", "offer", "rejected", "withdrawn", "skipped",
    "archived",
}
EMAIL_CATEGORIES = {
    "application_received", "assessment", "action_required", "interview", "recruiter_outreach",
    "rejection", "offer", "other",
}
ACTIVE = {"ready_for_application", "ready_for_review", "applied", "assessment", "interview", "offer"}
NOT_APPLIED = {"discovered", "saved", "preparing", "ready_for_application", "ready_for_review"}


def read_tracker(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_tracker(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=TRACKER_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def output(rows: list[dict[str, str]]) -> None:
    if not rows:
        print("No matching application records.")
        return
    for row in rows:
        print(f"{row['role_id']} | {row['status']} | {row['company']} | {row['role_title']} | next: {row['next_action']}")


def applied_date(pack: Path) -> str:
    job_file = pack / "job.yaml"
    if not job_file.exists():
        return ""
    match = re.search(r"^  applied:\s*\"?([^\n\"]+)\"?\s*$", job_file.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1).strip() if match else ""


def classify(subject: str, snippet: str) -> str:
    text = f"{subject} {snippet}".lower()
    if any(term in text for term in ("assessment", "coding challenge", "online test")):
        return "assessment"
    if any(term in text for term in ("interview", "schedule a call", "schedule time")):
        return "interview"
    if any(term in text for term in ("offer", "offer letter")):
        return "offer"
    if any(term in text for term in ("not moving forward", "not selected", "regret to inform", "rejection")):
        return "rejection"
    if any(term in text for term in ("action required", "complete", "additional information")):
        return "action_required"
    if any(term in text for term in ("application received", "application confirmation", "thank you for applying")):
        return "application_received"
    if any(term in text for term in ("recruiter", "opportunity", "your background")):
        return "recruiter_outreach"
    return "other"


def append_email_event(pack: Path, received: str, category: str, reference: str, subject: str) -> None:
    event_file = pack / "05_provenance" / "email-events.md"
    summary = subject.replace("|", "/").replace("\n", " ").strip() or "No subject supplied"
    with event_file.open("a", encoding="utf-8") as stream:
        stream.write(f"\n| {received} | {category} | {reference} | {summary} | none |\n")
    with (pack / "application-log.md").open("a", encoding="utf-8") as stream:
        stream.write(f"\n{date.today()} — Email event recorded: {category}; reference: {reference}. No status changed.\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Query local application state or record a minimal email event.")
    parser.add_argument("--workspace", required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("summary")
    subparsers.add_parser("needs-action")
    subparsers.add_parser("awaiting-response")
    subparsers.add_parser("not-applied")
    stage = subparsers.add_parser("stage")
    stage.add_argument("--status", required=True, choices=sorted(VALID_STATUSES))
    monthly = subparsers.add_parser("applied-count")
    monthly.add_argument("--month", required=True, help="YYYY-MM")
    email = subparsers.add_parser("record-email")
    email.add_argument("--role-id", required=True)
    email.add_argument("--received", required=True, help="YYYY-MM-DD")
    email.add_argument("--message-reference", required=True, help="Provider message ID or user-supplied reference")
    email.add_argument("--subject", default="")
    email.add_argument("--snippet", default="")
    email.add_argument("--category", default="auto", choices=["auto", *sorted(EMAIL_CATEGORIES)])
    update = subparsers.add_parser("set-status")
    update.add_argument("--role-id", required=True)
    update.add_argument("--status", required=True, choices=sorted(VALID_STATUSES - {"applied"}))
    update.add_argument("--reason", required=True)
    update.add_argument("--user-confirmation", required=True, help="Records the user's confirmation of this status change.")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    tracker_path = workspace / "tracker.csv"
    rows = read_tracker(tracker_path)

    if args.command == "summary":
        output(rows)
    elif args.command == "needs-action":
        output([row for row in rows if row["status"] in NOT_APPLIED or row["next_action"] not in {"", "unknown"}])
    elif args.command == "awaiting-response":
        output([row for row in rows if row["status"] == "applied"])
    elif args.command == "not-applied":
        output([row for row in rows if row["status"] in NOT_APPLIED])
    elif args.command == "stage":
        output([row for row in rows if row["status"] == args.status])
    elif args.command == "applied-count":
        count = sum(applied_date(workspace / row["application_pack_path"]).startswith(args.month) for row in rows if row["status"] == "applied")
        print(f"Applications submitted in {args.month}: {count}")
    elif args.command == "record-email":
        matches = [row for row in rows if row["role_id"] == args.role_id]
        if len(matches) != 1:
            parser.error(f"expected exactly one tracker record for {args.role_id}")
        category = classify(args.subject, args.snippet) if args.category == "auto" else args.category
        append_email_event(workspace / matches[0]["application_pack_path"], args.received, category, args.message_reference, args.subject)
        print(f"Recorded {category} email event for {args.role_id}. No status changed.")
    else:
        matches = [row for row in rows if row["role_id"] == args.role_id]
        if len(matches) != 1:
            parser.error(f"expected exactly one tracker record for {args.role_id}")
        row = matches[0]
        row["status"] = args.status
        row["next_action"] = "Review latest employer update"
        pack = workspace / row["application_pack_path"]
        job_file = pack / "job.yaml"
        job_text = re.sub(r"^status:.*$", f"status: {args.status}", job_file.read_text(encoding="utf-8"), flags=re.MULTILINE)
        job_file.write_text(job_text, encoding="utf-8")
        with (pack / "application-log.md").open("a", encoding="utf-8") as stream:
            stream.write(
                f"\n{date.today()} — Status set to {args.status}: {args.reason} "
                f"User confirmation: {args.user_confirmation}\n"
            )
        write_tracker(tracker_path, rows)
        print(f"Set {args.role_id} to {args.status}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
