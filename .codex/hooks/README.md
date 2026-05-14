# Codex Guarded Hooks

This repository uses Codex hooks as a local guardrail around the dataset and
publication metadata surfaces. The canonical validation rules stay in
`scripts/validate_dataset.py`, `scripts/render_metadata.py`, and
`scripts/release_check.py`; the hook only decides when those checks should run
or when a write is structurally unsafe.

Codex loads hook routing from `.codex/config.toml` and `.codex/hooks.json` for
trusted worktrees. After adding or changing hook routing, start a fresh Codex
session in this repository if the current session does not appear to run them.

## Blocking Rules

Pre-write hooks block:

- direct Codex edits to `.zenodo.json` or `CITATION.cff`; edit
  `data/metadata.json` and run `python scripts\render_metadata.py --write`
  instead.
- new `data/searches/*.json` artifacts unless `data/searches/index.json` is
  touched in the same write or patch.
- new `data/tezkire_extracts/*.md` extracts unless
  `data/tezkire_extracts/index.json` is touched in the same write or patch.

Post-write hooks run `python scripts\validate_dataset.py` after relevant
file-tool edits to `README.md`, `data/**`, or the release/metadata scripts.
They also watch shell-style tools (`Bash`, `shell_command`, `unified_exec`,
and `exec_command`) after the command finishes; if those commands leave watched
release paths dirty, the hook runs `python scripts\release_check.py`.

On `Stop`, the hook runs `python scripts\release_check.py` when watched release
paths are dirty, including `data/**`, `scripts/**`, `.codex/**`, `tests/**`,
README/release metadata files, and the release checklist.

## Advisory Mode

For temporary repairs, set:

```powershell
$env:JWC_HOOK_MODE = "advisory"
```

Advisory mode turns pre-write denials into warnings, while post-write and stop
validation still run.
