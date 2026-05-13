# Release Guardrails Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent future count drift, schema drift, stale status claims, and publication-metadata divergence in the Jahanshah witness census deposit.

**Architecture:** Keep the research data hand-curated, but add a small canonical metadata layer and release tooling. `data/metadata.json` is the source for publication metadata; `scripts/render_metadata.py` renders `.zenodo.json` and `CITATION.cff`; `scripts/validate_dataset.py` enforces structural consistency; `scripts/release_check.py` runs the full release gate.

**Tech Stack:** Python standard library only, JSON, YAML-as-text rendering for CFF, existing Markdown/JSON repo artifacts.

---

### Task 1: Canonical Metadata And Renderer

**Files:**
- Create: `data/metadata.json`
- Create: `scripts/render_metadata.py`
- Modify: `scripts/validate_dataset.py`

- [ ] **Step 1: Write failing validator checks**

Add checks that fail unless `data/metadata.json` exists, exposes title/version/doi/authors/description fields, and rendered `.zenodo.json` plus `CITATION.cff` match the generator.

- [ ] **Step 2: Run failing check**

Run: `python scripts\validate_dataset.py`
Expected: fail with missing metadata/generator checks.

- [ ] **Step 3: Implement renderer**

Create `scripts/render_metadata.py` with `--check` and `--write`. It reads `data/metadata.json` and `data/witness_register.json`, renders `.zenodo.json` and `CITATION.cff`, and returns nonzero when checked files are stale.

- [ ] **Step 4: Run passing check**

Run: `python scripts\validate_dataset.py`
Expected: pass.

### Task 2: Release Check Command

**Files:**
- Create: `scripts/release_check.py`
- Create: `docs/release-checklist.md`
- Modify: `README.md`
- Modify: `data/README.md`

- [ ] **Step 1: Write failing validator check**

Extend `validate_dataset.py` to require the release check script and checklist.

- [ ] **Step 2: Run failing check**

Run: `python scripts\validate_dataset.py`
Expected: fail with missing release-check assets.

- [ ] **Step 3: Implement release gate**

Create `scripts/release_check.py` to run dataset validation, metadata render check, JSON parsing, and `git diff --check`.

- [ ] **Step 4: Document release workflow**

Add `docs/release-checklist.md` and update docs to point users at `python scripts\release_check.py`.

- [ ] **Step 5: Run final verification**

Run:
- `python scripts\validate_dataset.py`
- `python scripts\render_metadata.py --check`
- `python scripts\release_check.py`
- `git diff --check`

Expected: all pass.
