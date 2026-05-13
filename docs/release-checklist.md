# Release Checklist

Run this checklist before publishing a new dataset version or making a release-style commit.

1. Update `data/witness_register.json` first. Keep terminal witness status in the register, not in README prose.
2. Update `data/spec.md` when register top-level fields or stat semantics change.
3. Add or update index entries for new evidence artifacts:
   - `data/searches/index.json` for search-session JSON files.
   - `data/tezkire_extracts/index.json` for tezkire Markdown extracts.
4. Mark superseded artifacts with `current_status_note` or `superseded_by` instead of deleting historical evidence.
5. Update `data/metadata.json` for publication metadata changes, then run `python scripts\render_metadata.py --write`.
6. Run `python scripts\release_check.py`.
7. Keep Codex hook guardrails current when validation behavior changes. Hook routing lives in `.codex/hooks.json`; the implementation lives in `.codex/hooks/guard.py`.
8. Read the staged diff before commit. Exclude local PDFs, source scans, and unrelated workspace files.

The release gate is intentionally local and dependency-free. It validates JSON parseability, register statistics, stale status phrases, search/extract indexes, publication metadata rendering, Codex hook tests, and whitespace issues in unstaged and staged changes.
