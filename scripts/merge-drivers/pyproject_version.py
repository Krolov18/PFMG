#!/usr/bin/env python3
"""Merge driver for pyproject.toml.

- Keeps the current branch's (ours) value for [project] version.
- Runs a normal 3-way merge for the rest; other conflicts are left as markers.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


def extract_project_version(content: str) -> str | None:
    """Extract the version value from the first [project] section."""
    in_project = False
    for line in content.splitlines():
        line_stripped = line.strip()
        if line_stripped == "[project]":
            in_project = True
            continue
        if in_project and line_stripped.startswith("["):
            break
        if in_project:
            m = re.match(r"version\s*=\s*[\"']([^\"']+)[\"']", line_stripped)
            if m:
                return m.group(1)
    return None


def replace_project_version_in_merged(merged: str, our_version: str) -> str:
    """Replace [project] version with our_version in merged content.

    Resolves conflict blocks that only concern the version line; leaves other
    conflict markers unchanged.
    """
    lines = merged.splitlines(keepends=True)
    result: list[str] = []
    i = 0
    in_project = False
    version_key_re = re.compile(r"^\s*version\s*=")

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped == "[project]":
            in_project = True
            result.append(line)
            i += 1
            continue

        if in_project and stripped.startswith("[") and stripped != "[project]":
            in_project = False

        # Conflict block that might contain version
        if in_project and stripped.startswith("<<<<<<<"):
            block: list[str] = [line]
            i += 1
            has_version = False
            while i < len(lines) and not lines[i].strip().startswith(">>>>>>>"):
                if version_key_re.match(lines[i]):
                    has_version = True
                block.append(lines[i])
                i += 1
            if i < len(lines):
                block.append(lines[i])
                i += 1
            if has_version:
                result.append(f'version = "{our_version}"\n')
            else:
                result.extend(block)
            continue

        # Single version line (no conflict)
        if in_project and version_key_re.match(line):
            result.append(f'version = "{our_version}"\n')
            i += 1
            continue

        result.append(line)
        i += 1

    return "".join(result)


def main() -> int:
    """Run merge driver: keep ours for [project] version, merge rest."""
    if len(sys.argv) != 5:
        sys.stderr.write("Usage: pyproject_version.py <base> <ours> <theirs> <path>\n")
        return 2
    base_path, ours_path, theirs_path, _path = sys.argv[1:5]

    ours_content = Path(ours_path).read_text()
    our_version = extract_project_version(ours_content)
    if our_version is None:
        sys.stderr.write("Merge driver: no [project] version in ours, aborting.\n")
        return 1

    # Paths come from git merge driver (trusted).
    git_cmd = shutil.which("git") or "git"
    result = subprocess.run(  # noqa: S603
        [git_cmd, "merge-file", "-p", ours_path, base_path, theirs_path],
        capture_output=True,
        text=True,
        check=False,
    )
    merged_content = result.stdout

    resolved = replace_project_version_in_merged(merged_content, our_version)
    Path(ours_path).write_text(resolved)

    # 0 = no conflict, 1 = conflicts (we resolved version; others may remain in file)
    return 0 if result.returncode in (0, 1) else result.returncode


if __name__ == "__main__":
    sys.exit(main())
