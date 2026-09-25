#!/usr/bin/env python3
"""Lightweight validation for a Career Application Pipeline workspace."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

REQUIRED = [
    "config.yaml",
    "cv/parsed-profile.yaml",
    "cv/search-criteria.yaml",
    "cv/reusable-answers.md",
    "cv/cv-feedback.md",
    "tracker.csv",
    "source-inventory.yaml",
    "application-field-rules.md",
    "applications",
    "roles/raw",
    "roles/staged",
    "roles/verified",
]

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate expected workspace files.")
    parser.add_argument("workspace")
    args = parser.parse_args()
    ws = Path(args.workspace).expanduser().resolve()

    errors = []
    for rel in REQUIRED:
        if not (ws / rel).exists():
            errors.append(f"missing: {rel}")

    tracker = ws / "tracker.csv"
    if tracker.exists():
        with tracker.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
        if headers != TRACKER_HEADERS:
            errors.append(f"tracker headers differ: {headers}")
        else:
            for row_number, row in enumerate(rows, start=2):
                status = row["status"].strip()
                if status not in VALID_STATUSES:
                    errors.append(f"invalid tracker status at row {row_number}: {status}")
                pack_path = row["application_pack_path"].strip()
                if pack_path:
                    pack = ws / pack_path
                    if not pack.is_dir():
                        errors.append(f"missing application pack at row {row_number}: {pack_path}")
                    else:
                        for name in ("job.yaml", "application-log.md"):
                            if not (pack / name).exists():
                                errors.append(f"application pack missing {name} at row {row_number}: {pack_path}")
                        report = pack / "02_background" / "preparation-report.md"
                        if not report.exists():
                            errors.append(f"application pack missing preparation report at row {row_number}: {pack_path}")

    rules = ws / "application-field-rules.md"
    if rules.exists():
        rule_text = rules.read_text(encoding="utf-8")
        for heading in ("GREEN", "YELLOW", "RED"):
            if heading not in rule_text:
                errors.append(f"application field rules missing category: {heading}")

    if errors:
        print("Workspace validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"Workspace validation passed: {ws}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
