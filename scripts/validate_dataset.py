#!/usr/bin/env python3
"""Validate high-level consistency for the witness census deposit."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path):
    return json.loads(read_text(path))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_json_parse(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.json")):
        try:
            load_json(path)
        except Exception as exc:  # pragma: no cover - diagnostic path
            fail(errors, f"{rel(path)} is invalid JSON: {exc}")


def validate_register(errors: list[str]) -> None:
    register_path = ROOT / "data" / "witness_register.json"
    register = load_json(register_path)
    witnesses = register["witnesses"]
    stats = register["stats"]

    actual_by_verification = Counter(w["verification_status"] for w in witnesses)
    for status, count in actual_by_verification.items():
        if stats["by_verification"].get(status) != count:
            fail(
                errors,
                f"stats.by_verification[{status!r}] is {stats['by_verification'].get(status)!r}, expected {count}",
            )

    nonzero_stored = {
        status: count for status, count in stats["by_verification"].items() if count
    }
    if nonzero_stored != dict(actual_by_verification):
        fail(
            errors,
            "stats.by_verification nonzero buckets do not match observed statuses",
        )

    non_rejected = [w for w in witnesses if w["verification_status"] != "rejected"]
    if stats.get("total_non_rejected_entries") != len(non_rejected):
        fail(
            errors,
            "stats.total_non_rejected_entries must equal non-rejected witness count",
        )
    if stats.get("total_witnesses_active") != len(non_rejected):
        fail(
            errors,
            "stats.total_witnesses_active must equal non-rejected witness count",
        )
    if stats.get("total_entries_including_rejected_and_lost") != len(witnesses):
        fail(
            errors,
            "stats.total_entries_including_rejected_and_lost must equal total witness entry count",
        )

    actual_by_completeness = Counter(w["completeness"] for w in non_rejected)
    nonzero_completeness = {
        completeness: count
        for completeness, count in stats["by_completeness"].items()
        if count
    }
    if nonzero_completeness != dict(actual_by_completeness):
        fail(
            errors,
            "stats.by_completeness nonzero buckets do not match active observed completeness values",
        )

    actual_by_country = Counter(w["country"] for w in non_rejected)
    nonzero_countries = {
        country: count
        for country, count in stats["by_country"].items()
        if count
    }
    if nonzero_countries != dict(actual_by_country):
        fail(
            errors,
            "stats.by_country nonzero buckets do not match active observed countries",
        )

    verified_or_caveated = sum(
        1
        for w in witnesses
        if w["verification_status"] in {"verified", "verified_with_attribution_caveat"}
    )
    if stats.get("total_verified_or_caveated_witnesses") != verified_or_caveated:
        fail(
            errors,
            "stats.total_verified_or_caveated_witnesses must equal verified plus caveated witnesses",
        )

    for witness in witnesses:
        for attestation in witness.get("scholarly_attestation", []):
            if attestation.get("year") == "n.d.":
                fail(
                    errors,
                    f"{witness['witness_id']} uses year='n.d.'; use null for unknown year",
                )
            if attestation.get("saw_firsthand", "__missing__") is None:
                fail(
                    errors,
                    f"{witness['witness_id']} uses saw_firsthand=null; omit it when unknown",
                )


def validate_spec(errors: list[str]) -> None:
    spec = read_text(ROOT / "data" / "spec.md")
    register = load_json(ROOT / "data" / "witness_register.json")
    generated = register["generated"]
    if f"Generated {generated}" not in spec:
        fail(errors, "data/spec.md generated date does not match witness_register.json")
    if '"candidate_inclusion_criterion"' not in spec:
        fail(errors, "data/spec.md top-level example omits candidate_inclusion_criterion")
    if "total_non_rejected_entries" not in spec:
        fail(errors, "data/spec.md does not document total_non_rejected_entries")


def validate_stale_text(errors: list[str]) -> None:
    stale_patterns = {
        "data/research_log/nuruosmaniye_04281_decoration_extract.md": [
            "Final register status: `candidate_probably_yusuf_hakiki_or_other_homonym`",
            "YEK shows `has_digitized_images: false`, so direct images are not available",
        ],
        "README.md": [
            "All nine Iranian portals were inaccessible",
            "nine remaining gaps that require on-site or in-person work",
        ],
        "data/searches/gap_disposition_2026-05-11.json": [
            "Gap disposition for 7 tool-shaped gaps",
            "All 10 tool-shaped gaps",
        ],
        "data/searches/probe_2026-05-11_avenues_rollup_summary.json": [
            "candidate_probably_yusuf_hakiki_or_other_homonym=1, rejected=2",
            "rejected=2 [total=14]",
        ],
    }
    for relative, patterns in stale_patterns.items():
        text = read_text(ROOT / relative)
        for pattern in patterns:
            if pattern in text:
                fail(errors, f"{relative} contains stale text: {pattern}")


def validate_gap_disposition(errors: list[str]) -> None:
    path = ROOT / "data" / "searches" / "gap_disposition_2026-05-11.json"
    data = load_json(path)
    gap_count = len(data["gaps"])
    summary_count = data["summary"]["total_gaps_addressed"]
    if summary_count != gap_count:
        fail(
            errors,
            f"{rel(path)} summary.total_gaps_addressed={summary_count}, expected {gap_count}",
        )
    if "companion_playwright_gaps_probed" not in data["summary"]:
        fail(errors, f"{rel(path)} summary must state companion Playwright gap count")


def validate_search_index(errors: list[str]) -> None:
    searches_dir = ROOT / "data" / "searches"
    index_path = searches_dir / "index.json"
    if not index_path.exists():
        fail(errors, "data/searches/index.json is missing")
        return

    index = load_json(index_path)
    indexed = {record["file"] for record in index.get("records", [])}
    actual = {
        path.name
        for path in searches_dir.glob("*.json")
        if path.name != "index.json"
    }
    missing = sorted(actual - indexed)
    extra = sorted(indexed - actual)
    if missing:
        fail(errors, f"data/searches/index.json missing records: {missing}")
    if extra:
        fail(errors, f"data/searches/index.json references missing files: {extra}")

    for record in index.get("records", []):
        if "current" not in record or "superseded_by" not in record:
            fail(errors, f"search index record lacks current/superseded_by: {record}")


def validate_teece_extract(errors: list[str]) -> None:
    path = ROOT / "data" / "extracts" / "teece_2016_pir_budaq_corpus.json"
    data = load_json(path)
    entries = data["appendix_b_pir_budaq_manuscripts"]["entries"]
    keys: dict[tuple[object, ...], list[int]] = defaultdict(list)
    for index, entry in enumerate(entries):
        key = (
            entry.get("shelfmark"),
            entry.get("current_location"),
            entry.get("text"),
            entry.get("date_ah"),
            entry.get("date_ce"),
        )
        keys[key].append(index)
    duplicates = {key: idxs for key, idxs in keys.items() if len(idxs) > 1}
    if duplicates:
        fail(errors, f"{rel(path)} has duplicate Appendix B compound keys: {duplicates}")


def validate_tezkire_index(errors: list[str]) -> None:
    directory = ROOT / "data" / "tezkire_extracts"
    index_path = directory / "index.json"
    if not index_path.exists():
        fail(errors, "data/tezkire_extracts/index.json is missing")
        return

    index = load_json(index_path)
    indexed = {record["file"] for record in index.get("records", [])}
    actual = {path.name for path in directory.glob("*.md")}
    missing = sorted(actual - indexed)
    extra = sorted(indexed - actual)
    if missing:
        fail(errors, f"data/tezkire_extracts/index.json missing records: {missing}")
    if extra:
        fail(errors, f"data/tezkire_extracts/index.json references missing files: {extra}")

    required = {"file", "source_type", "source_citation", "access", "extraction_date"}
    for record in index.get("records", []):
        missing_fields = sorted(required - record.keys())
        if missing_fields:
            fail(
                errors,
                f"tezkire index record for {record.get('file', '<unknown>')} missing {missing_fields}",
            )


def validate_metadata_surface(errors: list[str]) -> None:
    metadata_path = ROOT / "data" / "metadata.json"
    if not metadata_path.exists():
        fail(errors, "data/metadata.json is missing")
        return

    metadata = load_json(metadata_path)
    required = {
        "title",
        "version",
        "doi",
        "license",
        "release_date",
        "authors",
        "keywords",
        "subjects",
        "related_identifiers",
        "intro",
        "search_key_summary",
        "alevi_summary",
        "methodology_summary",
    }
    missing = sorted(required - metadata.keys())
    if missing:
        fail(errors, f"data/metadata.json missing fields: {missing}")

    if len(metadata.get("authors", [])) < 1:
        fail(errors, "data/metadata.json must define at least one author")

    renderer = ROOT / "scripts" / "render_metadata.py"
    if not renderer.exists():
        fail(errors, "scripts/render_metadata.py is missing")
        return

    result = subprocess.run(
        [sys.executable, str(renderer), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        fail(errors, f"render_metadata.py --check failed:\n{result.stdout.strip()}")


def validate_release_assets(errors: list[str]) -> None:
    required = [
        ROOT / "scripts" / "release_check.py",
        ROOT / "docs" / "release-checklist.md",
    ]
    for path in required:
        if not path.exists():
            fail(errors, f"{rel(path)} is missing")


def main() -> int:
    errors: list[str] = []
    validate_json_parse(errors)
    validate_register(errors)
    validate_spec(errors)
    validate_stale_text(errors)
    validate_gap_disposition(errors)
    validate_search_index(errors)
    validate_teece_extract(errors)
    validate_tezkire_index(errors)
    validate_metadata_surface(errors)
    validate_release_assets(errors)

    if errors:
        print("Dataset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Dataset validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
