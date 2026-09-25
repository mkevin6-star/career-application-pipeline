#!/usr/bin/env python3
"""Initialize a Career Application Pipeline workspace.

This script is dependency-free and copies repository templates into a user
workspace. It does not parse CVs or call external services.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"


def copy_if_missing(src: Path, dst: Path, force: bool = False) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not force:
        return
    shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a job-search workspace from templates.")
    parser.add_argument("--workspace", required=True, help="Workspace directory to create/use")
    parser.add_argument("--force", action="store_true", help="Overwrite existing templated files")
    args = parser.parse_args()

    ws = Path(args.workspace).expanduser().resolve()
    ws.mkdir(parents=True, exist_ok=True)

    dirs = [
        "cv/original",
        "roles/raw",
        "roles/staged",
        "roles/verified",
        "applications",
        "templates/application-pack",
        "logs",
    ]
    for d in dirs:
        (ws / d).mkdir(parents=True, exist_ok=True)

    mapping = {
        TEMPLATES / "workspace-config.yaml": ws / "config.yaml",
        TEMPLATES / "candidate-profile.yaml": ws / "cv/parsed-profile.yaml",
        TEMPLATES / "search-criteria.yaml": ws / "cv/search-criteria.yaml",
        TEMPLATES / "reusable-answers.md": ws / "cv/reusable-answers.md",
        TEMPLATES / "cv-feedback.md": ws / "cv/cv-feedback.md",
        TEMPLATES / "tracker.csv": ws / "tracker.csv",
        TEMPLATES / "source-inventory.yaml": ws / "source-inventory.yaml",
        TEMPLATES / "application-field-rules.md": ws / "application-field-rules.md",
        TEMPLATES / "cover-letter-styles.yaml": ws / "templates/cover-letter-styles.yaml",
    }
    for src, dst in mapping.items():
        copy_if_missing(src, dst, args.force)

    app_src = TEMPLATES / "application-pack"
    app_dst = ws / "templates/application-pack"
    for src in app_src.rglob("*"):
        if src.is_file():
            copy_if_missing(src, app_dst / src.relative_to(app_src), args.force)

    print(f"Workspace initialized: {ws}")
    print("Next: give AGENT_PLAYBOOK.md to your agent with the workspace path and CV source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
