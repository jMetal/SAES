#!/usr/bin/env python3
"""Stamp CHANGELOG.md and bump version.txt for a release.

Usage:
    python scripts/release_stamp.py --bump minor --author @username
    python scripts/release_stamp.py --dry-run
    python scripts/release_stamp.py --bump patch --author @ci-bot --date 2026-04-19
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


def _git_user() -> str:
    """Get the current git user name as a fallback author."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%an"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stamp CHANGELOG.md and bump version.txt for a release.",
    )
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        default="minor",
        help="Version component to bump (default: minor)",
    )
    parser.add_argument(
        "--author",
        default=None,
        help="Author to credit in the changelog (default: git user)",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Release date in YYYY-MM-DD format (default: today UTC)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    parser.add_argument(
        "--version-file",
        default="version.txt",
        help="Path to version.txt (default: version.txt)",
    )
    parser.add_argument(
        "--changelog-file",
        default="CHANGELOG.md",
        help="Path to CHANGELOG.md (default: CHANGELOG.md)",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    # ── Read current version ────────────────────────────────────
    version_file = Path(args.version_file)
    if not version_file.exists():
        print(f"ERROR: {version_file} not found")
        return 1

    current = version_file.read_text().strip()
    base_version = current

    # Validate semver format
    parts = base_version.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        print(f"ERROR: invalid semver format (got: {base_version})")
        return 1

    major, minor, patch = (int(p) for p in parts)

    # ── Compute release version ─────────────────────────────────
    if args.bump == "major":
        new_major, new_minor, new_patch = major + 1, 0, 0
    elif args.bump == "minor":
        new_major, new_minor, new_patch = major, minor + 1, 0
    else:  # patch
        new_major, new_minor, new_patch = major, minor, patch + 1

    release = f"{new_major}.{new_minor}.{new_patch}"
    next_version = release

    author = args.author or _git_user()
    date = args.date or datetime.now(tz=UTC).strftime("%Y-%m-%d")

    # ── Summary ─────────────────────────────────────────────────
    print("=== Release Stamp ===")
    print(f"  Current:  {current}")
    print(f"  Release:  {release}")
    print(f"  Next:     {next_version}")
    print(f"  Bump:     {args.bump}")
    print(f"  Author:   {author}")
    print(f"  Date:     {date}")

    if args.dry_run:
        print("\n[DRY RUN] No files modified.")
        return 0

    # ── Process CHANGELOG.md ────────────────────────────────────
    changelog_file = Path(args.changelog_file)
    if not changelog_file.exists():
        print(f"ERROR: {changelog_file} not found")
        return 1

    content = changelog_file.read_text()

    # Locate the ## [Unreleased] header
    marker = "## [Unreleased]"
    marker_idx = content.find(marker)
    if marker_idx == -1:
        print("ERROR: No '## [Unreleased]' section found in CHANGELOG.md")
        return 1

    marker_end = marker_idx + len(marker)

    # Find the next version section header (## [x.y.z]) after [Unreleased]
    next_section = re.search(r"\n## \[", content[marker_end:])

    if next_section:
        # Entries live between [Unreleased] header and next ## [
        entries_end = marker_end + next_section.start()
        entries = content[marker_end:entries_end].strip()
        after = content[entries_end:]  # includes the \n## [x.y.z]...
    else:
        # No previous releases — entries go to end of file
        entries = content[marker_end:].strip()
        after = ""

    # If no entries, add a default message
    if not entries:
        entries = "- No updates for this version"

    # Rebuild: everything before [Unreleased] + new [Unreleased] + stamped release
    before = content[:marker_idx]
    content = f"{before}## [Unreleased]\n\n## [{release}] — {date} ({author})\n\n{entries}\n{after}"

    # ── Write files ─────────────────────────────────────────────
    changelog_file.write_text(content)
    version_file.write_text(f"{next_version}\n")

    pyproject_file = Path("pyproject.toml")
    if pyproject_file.exists():
        toml_content = pyproject_file.read_text()
        # Regex to find version = "..." in the [project] section
        # Using a non-greedy match to ensure we only hit the first occurrence (usually [project])
        new_toml = re.sub(
            r'(^version\s*=\s*")[^"]+(")',
            rf"\g<1>{release}\g<2>",
            toml_content,
            count=1,
            flags=re.MULTILINE,
        )
        if new_toml != toml_content:
            pyproject_file.write_text(new_toml)
            print(f"✅ pyproject.toml updated to {release}")

            # Run uv lock to update uv.lock
            try:
                subprocess.run(["uv", "lock"], check=True, capture_output=True)
                print("✅ uv.lock updated")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️ Could not update uv.lock (uv not found or lock failed)")
        else:
            print("⚠️ Could not find version field in pyproject.toml")

    print(f"\n✅ Changelog stamped as {release}")
    print(f"✅ Version bumped to {next_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
