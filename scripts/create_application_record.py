#!/usr/bin/env python3
"""Create or materialize auditable application-pack records.

The script is dependency-free. It never opens browsers, creates external
accounts, uploads documents, or submits applications.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "application-pack"
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


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def canonical_url(value: str) -> str:
    if not value:
        return ""
    parts = urlsplit(value)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), "", ""))


def yaml_string(value: str | None) -> str:
    return "null" if value is None else json.dumps(value)


def read_tracker(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_tracker(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=TRACKER_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def find_duplicate(rows: list[dict[str, str]], company: str, role: str, location: str, source_url: str, application_url: str) -> dict[str, str] | None:
    source = canonical_url(source_url)
    application = canonical_url(application_url)
    for row in rows:
        if source and source == canonical_url(row["source_url"]):
            return row
        if application and application == canonical_url(row["application_url"]):
            return row
        if (normalize(company), normalize(role), normalize(location)) == (
            normalize(row["company"]), normalize(row["role_title"]), normalize(row["location"])
        ):
            return row
    return None


def write_job_record(pack: Path, row: dict[str, str], discovered: str) -> None:
    job_file = pack / "job.yaml"
    job_is_template = job_file.exists() and 'role_id: unknown' in job_file.read_text(encoding="utf-8")
    if not job_file.exists() or job_is_template:
        job_file.write_text(
            "\n".join([
                f"role_id: {yaml_string(row['role_id'])}",
                f"company: {yaml_string(row['company'])}",
                f"role: {yaml_string(row['role_title'])}",
                f"location: {yaml_string(row['location'])}",
                "job_id: unknown",
                f"job_url: {yaml_string(row['source_url'])}",
                f"application_url: {yaml_string(row['application_url'])}",
                f"status: {row['status']}",
                "",
                "dates:",
                f"  discovered: {yaml_string(discovered)}",
                "  prepared: null",
                "  applied: null",
                "",
                "account:",
                "  created: false",
                "  email: unknown",
                "",
                "application:",
                "  resume_version: unknown",
                "  browser_started: false",
                f"  ready_for_review: {'true' if row['status'] == 'ready_for_review' else 'false'}",
                "  submitted: false",
                "",
                "unknowns: []",
                "",
            ]),
            encoding="utf-8",
        )

    log_file = pack / "application-log.md"
    log_is_template = log_file.exists() and "<!-- YYYY-MM-DD" in log_file.read_text(encoding="utf-8")
    if not log_file.exists() or log_is_template:
        log_file.write_text(
            "# Application Log\n\n"
            "Record material job-search events here without passwords, authentication codes, government IDs, or other secrets.\n\n"
            f"{discovered} — Job record materialized from tracker; status: {row['status']}.\n",
            encoding="utf-8",
        )


def copy_template(pack: Path) -> None:
    """Seed missing template files without replacing existing draft material."""
    for source in TEMPLATES.rglob("*"):
        destination = pack / source.relative_to(TEMPLATES)
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def materialize_existing(workspace: Path) -> int:
    tracker = workspace / "tracker.csv"
    rows = read_tracker(tracker)
    count = 0
    for row in rows:
        pack_path = row["application_pack_path"].strip()
        if not pack_path:
            continue
        pack = workspace / pack_path
        pack.mkdir(parents=True, exist_ok=True)
        copy_template(pack)
        write_job_record(pack, row, row["date_seen"] or str(date.today()))
        count += 1
    print(f"Materialized {count} application record(s).")
    return 0


def show_status(workspace: Path, role_id: str | None) -> int:
    rows = read_tracker(workspace / "tracker.csv")
    if role_id:
        rows = [row for row in rows if row["role_id"] == role_id]
        if not rows:
            print(f"No tracker record found for role_id: {role_id}")
            return 1

    for row in rows:
        print(f"{row['role_id']} | {row['status']} | {row['company']} | {row['role_title']}")
    return 0


def create_record(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).expanduser().resolve()
    tracker = workspace / "tracker.csv"
    rows = read_tracker(tracker)
    duplicate = find_duplicate(rows, args.company, args.role, args.location, args.source_url, args.application_url)
    if duplicate:
        print("Probable duplicate found:")
        print(f"- role_id: {duplicate['role_id']}")
        print(f"- status: {duplicate['status']}")
        print(f"- application_pack_path: {duplicate['application_pack_path']}")
        return 2

    discovered = args.discovered or str(date.today())
    role_id = f"{discovered}_{slug(args.company)}_{slug(args.role)}"
    relative_pack = Path("applications") / f"{discovered}_{slug(args.company)}_{slug(args.role)}"
    pack = workspace / relative_pack
    copy_template(pack)
    row = {
        "role_id": role_id,
        "date_seen": discovered,
        "last_seen": discovered,
        "company": args.company,
        "role_title": args.role,
        "location": args.location,
        "remote_policy": args.remote_policy,
        "source_url": args.source_url,
        "application_url": args.application_url or args.source_url,
        "score": "unknown",
        "status": args.status,
        "next_action": "Review role and prepare application materials",
        "follow_up_date": "unknown",
        "application_pack_path": relative_pack.as_posix(),
        "notes": "Created by create_application_record.py.",
    }
    write_job_record(pack, row, discovered)
    rows.append(row)
    write_tracker(tracker, rows)
    print(f"Created application record: {relative_pack}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or materialize application-pack records.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--materialize-existing", action="store_true")
    parser.add_argument("--show-status", action="store_true")
    parser.add_argument("--role-id")
    parser.add_argument("--company")
    parser.add_argument("--role")
    parser.add_argument("--location", default="unknown")
    parser.add_argument("--source-url")
    parser.add_argument("--application-url", default="")
    parser.add_argument("--remote-policy", default="unknown")
    parser.add_argument("--status", default="discovered", choices=sorted(VALID_STATUSES))
    parser.add_argument("--discovered")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    if args.show_status:
        return show_status(workspace, args.role_id)
    if args.materialize_existing:
        return materialize_existing(workspace)
    required = {"--company": args.company, "--role": args.role, "--source-url": args.source_url}
    missing = [flag for flag, value in required.items() if not value]
    if missing:
        parser.error("creation requires " + ", ".join(missing))
    return create_record(args)


if __name__ == "__main__":
    raise SystemExit(main())
