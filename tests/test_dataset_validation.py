from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_dataset.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_dataset", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("Unable to load scripts/validate_dataset.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DatasetValidationTests(unittest.TestCase):
    def test_spec_example_does_not_use_nd_year(self) -> None:
        spec = (ROOT / "data" / "spec.md").read_text(encoding="utf-8")

        self.assertNotIn('"year": "n.d."', spec)

    def test_validate_register_rejects_stale_total_active_alias(self) -> None:
        validator = load_validator()
        register = validator.load_json(ROOT / "data" / "witness_register.json")
        broken = copy.deepcopy(register)
        broken["stats"]["total_witnesses_active"] += 1

        with mock.patch.object(validator, "load_json", return_value=broken):
            errors: list[str] = []
            validator.validate_register(errors)

        self.assertTrue(
            any("stats.total_witnesses_active" in error for error in errors),
            errors,
        )

    def test_validate_register_rejects_stale_total_entries(self) -> None:
        validator = load_validator()
        register = validator.load_json(ROOT / "data" / "witness_register.json")
        broken = copy.deepcopy(register)
        broken["stats"]["total_entries_including_rejected_and_lost"] += 1

        with mock.patch.object(validator, "load_json", return_value=broken):
            errors: list[str] = []
            validator.validate_register(errors)

        self.assertTrue(
            any(
                "stats.total_entries_including_rejected_and_lost" in error
                for error in errors
            ),
            errors,
        )

    def test_validate_register_rejects_stale_completeness_counts(self) -> None:
        validator = load_validator()
        register = validator.load_json(ROOT / "data" / "witness_register.json")
        broken = copy.deepcopy(register)
        broken["stats"]["by_completeness"]["complete"] += 1

        with mock.patch.object(validator, "load_json", return_value=broken):
            errors: list[str] = []
            validator.validate_register(errors)

        self.assertTrue(
            any("stats.by_completeness" in error for error in errors),
            errors,
        )

    def test_validate_register_rejects_stale_country_counts(self) -> None:
        validator = load_validator()
        register = validator.load_json(ROOT / "data" / "witness_register.json")
        broken = copy.deepcopy(register)
        broken["stats"]["by_country"]["Turkey"] += 1

        with mock.patch.object(validator, "load_json", return_value=broken):
            errors: list[str] = []
            validator.validate_register(errors)

        self.assertTrue(any("stats.by_country" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
