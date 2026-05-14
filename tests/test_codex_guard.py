from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = ROOT / ".codex" / "hooks" / "guard.py"
RELEASE_CHECK_PATH = ROOT / "scripts" / "release_check.py"


def load_guard():
    spec = importlib.util.spec_from_file_location("codex_guard", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("Unable to load .codex/hooks/guard.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_release_check():
    spec = importlib.util.spec_from_file_location("release_check", RELEASE_CHECK_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("Unable to load scripts/release_check.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CodexGuardTests(unittest.TestCase):
    def test_apply_patch_extracts_every_target(self) -> None:
        guard = load_guard()
        payload = {
            "tool_name": "apply_patch",
            "tool_input": {
                "patch": "\n".join(
                    [
                        "*** Begin Patch",
                        "*** Update File: README.md",
                        "@@",
                        "-old",
                        "+new",
                        "*** Add File: data/searches/new_probe.json",
                        "+{}",
                        "*** Delete File: data/searches/old_probe.json",
                        "*** Move to: data/searches/renamed_probe.json",
                        "*** End Patch",
                    ]
                )
            },
        }

        touches = guard.extract_touches(payload)

        self.assertEqual(
            [(touch.action, touch.path) for touch in touches],
            [
                ("update", "README.md"),
                ("add", "data/searches/new_probe.json"),
                ("delete", "data/searches/old_probe.json"),
                ("move", "data/searches/renamed_probe.json"),
            ],
        )

    def test_preflight_blocks_direct_generated_metadata_edit(self) -> None:
        guard = load_guard()
        payload = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Edit",
            "tool_input": {"file_path": str(ROOT / ".zenodo.json")},
        }

        decision = guard.preflight(payload, ROOT)

        self.assertFalse(decision.allowed)
        self.assertIn("data/metadata.json", decision.reason)
        self.assertIn("render_metadata.py --write", decision.reason)

    def test_preflight_blocks_relative_generated_metadata_paths(self) -> None:
        guard = load_guard()
        for path in [".zenodo.json", "./.zenodo.json"]:
            with self.subTest(path=path):
                payload = {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Edit",
                    "tool_input": {"file_path": path},
                }

                decision = guard.preflight(payload, ROOT)

                self.assertFalse(decision.allowed)
                self.assertIn("data/metadata.json", decision.reason)

    def test_preflight_requires_index_update_for_new_search_json(self) -> None:
        guard = load_guard()
        payload = {
            "hook_event_name": "PreToolUse",
            "tool_name": "apply_patch",
            "tool_input": {
                "patch": "\n".join(
                    [
                        "*** Begin Patch",
                        "*** Add File: data/searches/new_probe.json",
                        "+{}",
                        "*** End Patch",
                    ]
                )
            },
        }

        decision = guard.preflight(payload, ROOT)

        self.assertFalse(decision.allowed)
        self.assertIn("data/searches/index.json", decision.reason)

    def test_preflight_allows_write_to_existing_search_json_without_index_update(self) -> None:
        guard = load_guard()
        payload = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "data/searches/gap_disposition_2026-05-11.json"},
        }

        decision = guard.preflight(payload, ROOT)

        self.assertTrue(decision.allowed)

    def test_postflight_runs_dataset_validation_for_data_edits(self) -> None:
        guard = load_guard()
        payload = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Edit",
            "tool_input": {"file_path": str(ROOT / "data" / "witness_register.json")},
        }
        completed = subprocess.CompletedProcess(
            args=[sys.executable, "scripts/validate_dataset.py"],
            returncode=0,
            stdout="dataset validation passed\n",
        )

        with mock.patch.object(guard.subprocess, "run", return_value=completed) as run:
            decision = guard.postflight(payload, ROOT)

        self.assertTrue(decision.allowed)
        run.assert_called_once()
        self.assertEqual(run.call_args.args[0], [sys.executable, "scripts/validate_dataset.py"])
        self.assertEqual(run.call_args.kwargs["cwd"], ROOT)

    def test_main_formats_pretool_denial_as_codex_json(self) -> None:
        guard = load_guard()
        payload = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": str(ROOT / "CITATION.cff")},
        }

        exit_code, stdout, stderr = guard.run(json.dumps(payload), ROOT)

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        parsed = json.loads(stdout)
        output = parsed["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "PreToolUse")
        self.assertEqual(output["permissionDecision"], "deny")
        self.assertIn("data/metadata.json", output["permissionDecisionReason"])

    def test_main_formats_posttool_failure_as_block_json(self) -> None:
        guard = load_guard()
        payload = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Edit",
            "tool_input": {"file_path": "data/witness_register.json"},
        }
        completed = subprocess.CompletedProcess(
            args=[sys.executable, "scripts/validate_dataset.py"],
            returncode=1,
            stdout="Dataset validation failed\n- bad stats\n",
        )

        with mock.patch.object(guard.subprocess, "run", return_value=completed):
            exit_code, stdout, stderr = guard.run(json.dumps(payload), ROOT)

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        parsed = json.loads(stdout)
        self.assertEqual(parsed["decision"], "block")
        self.assertIn("bad stats", parsed["reason"])
        self.assertNotIn("hookSpecificOutput", parsed)

    def test_dirty_release_paths_detects_staged_untracked_hook_and_test_changes(self) -> None:
        guard = load_guard()
        completed = subprocess.CompletedProcess(
            args=["git", "status", "--porcelain", "--untracked-files=all"],
            returncode=0,
            stdout="\n".join(
                [
                    "A  tests/test_codex_guard.py",
                    "?? .codex/hooks/guard.py",
                    "M  README.md",
                    "?? scratch.txt",
                ]
            ),
        )

        with mock.patch.object(guard.subprocess, "run", return_value=completed) as run:
            dirty = guard._dirty_release_paths(ROOT)

        self.assertEqual(
            set(dirty),
            {"tests/test_codex_guard.py", ".codex/hooks/guard.py", "README.md"},
        )
        run.assert_called_once()
        self.assertEqual(
            run.call_args.args[0],
            ["git", "status", "--porcelain", "--untracked-files=all"],
        )

    def test_shell_postflight_runs_release_check_when_release_paths_are_dirty(self) -> None:
        guard = load_guard()
        payload = {
            "hook_event_name": "PostToolUse",
            "tool_name": "shell_command",
            "tool_input": {"command": "Set-Content .zenodo.json '{}'"},
        }
        calls: list[list[str]] = []

        def fake_run(command: list[str], root: Path):
            calls.append(command)
            return guard.Decision(True)

        with (
            mock.patch.object(guard, "_dirty_release_paths", return_value=[".zenodo.json"]),
            mock.patch.object(guard, "_run", side_effect=fake_run),
        ):
            decision = guard.postflight(payload, ROOT)

        self.assertTrue(decision.allowed)
        self.assertEqual(calls, [[sys.executable, "scripts/release_check.py"]])

    def test_hooks_json_posttool_covers_shell_tool_names(self) -> None:
        hooks = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
        matcher = hooks["hooks"]["PostToolUse"][0]["matcher"]

        self.assertIn("shell_command", matcher)
        self.assertIn("unified_exec", matcher)
        self.assertIn("Bash", matcher)


class ReleaseCheckTests(unittest.TestCase):
    def test_release_check_runs_cached_diff_check(self) -> None:
        release_check = load_release_check()
        commands: list[list[str]] = []

        def fake_run_command(command: list[str]) -> int:
            commands.append(command)
            return 0

        with (
            mock.patch.object(release_check, "run_command", side_effect=fake_run_command),
            mock.patch.object(release_check, "parse_all_json", return_value=0),
            redirect_stdout(io.StringIO()),
        ):
            exit_code = release_check.main()

        self.assertEqual(exit_code, 0)
        self.assertIn(["git", "diff", "--check"], commands)
        self.assertIn(["git", "diff", "--cached", "--check"], commands)


if __name__ == "__main__":
    unittest.main()
