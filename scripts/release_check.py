#!/usr/bin/env python3
"""Run the publication release gate for the witness census deposit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_command(command: list[str]) -> int:
    print(f"$ {' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result.returncode


def parse_all_json() -> int:
    print("$ parse all JSON files")
    failures: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT).as_posix()}: {exc}")
    if failures:
        print("JSON parse failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("JSON parse ok")
    return 0


def main() -> int:
    commands = [
        [sys.executable, "scripts/validate_dataset.py"],
        [sys.executable, "scripts/render_metadata.py", "--check"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
    ]

    failures = 0
    for command in commands:
        failures += 1 if run_command(command) != 0 else 0
    failures += 1 if parse_all_json() != 0 else 0
    failures += 1 if run_command(["git", "diff", "--check"]) != 0 else 0
    failures += 1 if run_command(["git", "diff", "--cached", "--check"]) != 0 else 0

    if failures:
        print(f"Release check failed: {failures} step(s) failed.")
        return 1

    print("Release check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
