#!/usr/bin/env python3
"""Codex hook guardrails for the Jahanshah witness census dataset."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATED_METADATA = {".zenodo.json", "CITATION.cff"}
WATCHED_RELEASE_PATHS = {
    "README.md",
    ".zenodo.json",
    "CITATION.cff",
    "docs/release-checklist.md",
}
SHELL_TOOL_NAMES = {"bash", "shell_command", "unified_exec", "exec_command"}


@dataclass(frozen=True)
class Touch:
    action: str
    path: str


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str = ""


def _as_tool_input(payload: dict) -> dict:
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    return tool_input if isinstance(tool_input, dict) else {}


def _normalize_path(value: str, root: Path = ROOT) -> str:
    path = Path(value)
    try:
        if path.is_absolute():
            return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        pass
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _patch_text(tool_input: dict) -> str:
    for key in ("patch", "input", "command"):
        value = tool_input.get(key)
        if isinstance(value, str):
            return value
    return ""


def _append_unique(touches: list[Touch], touch: Touch) -> None:
    if touch not in touches:
        touches.append(touch)


def _extract_apply_patch_touches(tool_input: dict, root: Path) -> list[Touch]:
    prefixes = {
        "*** Add File: ": "add",
        "*** Update File: ": "update",
        "*** Delete File: ": "delete",
        "*** Move to: ": "move",
    }
    touches: list[Touch] = []
    for raw_line in _patch_text(tool_input).splitlines():
        for prefix, action in prefixes.items():
            if raw_line.startswith(prefix):
                path = _normalize_path(raw_line[len(prefix):].strip(), root)
                if path:
                    _append_unique(touches, Touch(action, path))
    return touches


def _extract_file_input_touches(tool_name: str, tool_input: dict, root: Path) -> list[Touch]:
    raw_paths: list[str] = []
    for key in ("file_path", "path", "file", "target"):
        value = tool_input.get(key)
        if isinstance(value, str):
            raw_paths.append(value)

    file_paths = tool_input.get("file_paths")
    if isinstance(file_paths, str):
        raw_paths.append(file_paths)
    elif isinstance(file_paths, list):
        raw_paths.extend(path for path in file_paths if isinstance(path, str))

    touches: list[Touch] = []
    for raw_path in raw_paths:
        path = _normalize_path(raw_path, root)
        if tool_name.lower() == "write":
            action = "update" if (root / path).exists() else "add"
        else:
            action = "edit"
        _append_unique(touches, Touch(action, path))
    return touches


def extract_touches(payload: dict, root: Path = ROOT) -> list[Touch]:
    tool_name = str(payload.get("tool_name") or payload.get("tool") or "")
    tool_input = _as_tool_input(payload)
    if tool_name == "apply_patch":
        return _extract_apply_patch_touches(tool_input, root)
    return _extract_file_input_touches(tool_name, tool_input, root)


def _is_shell_tool(tool_name: str) -> bool:
    normalized = tool_name.strip().lower()
    return normalized in SHELL_TOOL_NAMES or normalized.endswith(".shell_command")


def _hook_mode() -> str:
    return os.environ.get("JWC_HOOK_MODE", "blocking").strip().lower()


def _guard_decision(reason: str) -> Decision:
    if _hook_mode() == "advisory":
        return Decision(True, f"ADVISORY: {reason}")
    return Decision(False, reason)


def _touches_path(touches: list[Touch], path: str) -> bool:
    return any(touch.path == path for touch in touches)


def _added_paths(touches: list[Touch]) -> set[str]:
    return {touch.path for touch in touches if touch.action == "add"}


def preflight(payload: dict, root: Path = ROOT) -> Decision:
    touches = extract_touches(payload, root)
    if not touches:
        return Decision(True)

    generated = sorted(touch.path for touch in touches if touch.path in GENERATED_METADATA)
    if generated:
        return _guard_decision(
            "Generated publication metadata is rendered output, not the editing source. "
            "Edit data/metadata.json, then run python scripts/render_metadata.py --write. "
            f"Blocked direct edit to: {', '.join(generated)}"
        )

    added = _added_paths(touches)
    new_searches = sorted(
        path
        for path in added
        if path.startswith("data/searches/")
        and path.endswith(".json")
        and path != "data/searches/index.json"
    )
    if new_searches and not _touches_path(touches, "data/searches/index.json"):
        return _guard_decision(
            "New search JSON artifacts must be indexed in data/searches/index.json "
            f"in the same edit. Missing index update for: {', '.join(new_searches)}"
        )

    new_tezkire = sorted(
        path
        for path in added
        if path.startswith("data/tezkire_extracts/")
        and path.endswith(".md")
    )
    if new_tezkire and not _touches_path(touches, "data/tezkire_extracts/index.json"):
        return _guard_decision(
            "New tezkire extracts must be indexed in data/tezkire_extracts/index.json "
            f"in the same edit. Missing index update for: {', '.join(new_tezkire)}"
        )

    return Decision(True)


def _is_validation_relevant(path: str) -> bool:
    return (
        path == "README.md"
        or path.startswith("data/")
        or path in {"scripts/validate_dataset.py", "scripts/render_metadata.py", "scripts/release_check.py"}
    )


def _run(command: list[str], root: Path) -> Decision:
    result = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode == 0:
        return Decision(True)
    output = result.stdout.strip()
    return Decision(False, output or f"Command failed: {' '.join(command)}")


def postflight(payload: dict, root: Path = ROOT) -> Decision:
    tool_name = str(payload.get("tool_name") or payload.get("tool") or "")
    touches = extract_touches(payload, root)
    if any(_is_validation_relevant(touch.path) for touch in touches):
        return _run([sys.executable, "scripts/validate_dataset.py"], root)
    if _is_shell_tool(tool_name) and _dirty_release_paths(root):
        return _run([sys.executable, "scripts/release_check.py"], root)
    return Decision(True)


def _dirty_release_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        return []
    dirty = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip().replace("\\", "/") if len(line) > 3 else line.strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        dirty.append(path)
    return [
        path
        for path in dirty
        if (
            path in WATCHED_RELEASE_PATHS
            or path.startswith("data/")
            or path.startswith("scripts/")
            or path.startswith(".codex/")
            or path.startswith("tests/")
        )
    ]


def stop_check(root: Path = ROOT) -> Decision:
    if not _dirty_release_paths(root):
        return Decision(True)
    return _run([sys.executable, "scripts/release_check.py"], root)


def _deny_json(event: str, reason: str) -> str:
    return json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": event,
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    )


def _stop_json(reason: str) -> str:
    return json.dumps({"decision": "block", "reason": reason})


def run(raw: str, root: Path = ROOT) -> tuple[int, str, str]:
    if not raw or not raw.strip():
        return 0, "", ""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        return 0, "", f"witness-census guard ignored invalid hook JSON: {exc}"

    event = str(payload.get("hook_event_name") or payload.get("event") or "")
    if event == "PreToolUse":
        decision = preflight(payload, root)
        if decision.allowed:
            stderr = decision.reason if decision.reason.startswith("ADVISORY:") else ""
            return 0, "", stderr
        return 0, _deny_json(event, decision.reason), ""

    if event == "PostToolUse":
        decision = postflight(payload, root)
        if decision.allowed:
            return 0, "", ""
        return 0, _stop_json(decision.reason), ""

    if event == "Stop":
        decision = stop_check(root)
        if decision.allowed:
            return 0, "", ""
        return 0, _stop_json(decision.reason), ""

    return 0, "", ""


def main() -> int:
    exit_code, stdout, stderr = run(sys.stdin.read(), ROOT)
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
