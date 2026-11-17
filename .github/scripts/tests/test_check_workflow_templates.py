"""Tests for check_workflow_templates.py. Run: python3 -m unittest discover -s .github/scripts/tests"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_workflow_templates import check

CALL = "uses: theapotheosisgroup/.github/.github/workflows/reusable-security.yml@main\n"


class CheckWorkflowTemplatesTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, stem: str, workflow: str | None, meta: object | None) -> None:
        if workflow is not None:
            (self.dir / f"{stem}.yml").write_text(workflow, encoding="utf-8")
        if meta is not None:
            text = meta if isinstance(meta, str) else json.dumps(meta)
            (self.dir / f"{stem}.properties.json").write_text(text, encoding="utf-8")

    def test_valid_template_passes(self) -> None:
        self.write(
            "ok", CALL, {"name": "OK", "description": "d", "iconName": "octicon gear"}
        )
        self.assertEqual(check(self.dir), [])

    def test_missing_metadata_fails(self) -> None:
        self.write("lonely", CALL, None)
        self.assertTrue(
            any("missing lonely.properties.json" in e for e in check(self.dir))
        )

    def test_orphan_metadata_fails(self) -> None:
        self.write("ok", CALL, {"name": "OK", "description": "d"})
        self.write("orphan", None, {"name": "O", "description": "d"})
        self.assertTrue(any("no matching orphan.yml" in e for e in check(self.dir)))

    def test_missing_description_fails(self) -> None:
        self.write("ok", CALL, {"name": "OK"})
        self.assertTrue(any("'description'" in e for e in check(self.dir)))

    def test_invalid_json_fails(self) -> None:
        self.write("ok", CALL, "{not json")
        self.assertTrue(any("invalid JSON" in e for e in check(self.dir)))

    def test_bad_regex_and_missing_icon_fail(self) -> None:
        self.write(
            "ok",
            CALL,
            {
                "name": "OK",
                "description": "d",
                "iconName": "nope",
                "filePatterns": ["("],
            },
        )
        errors = check(self.dir)
        self.assertTrue(any("not a valid regex" in e for e in errors))
        self.assertTrue(any("has no nope.svg" in e for e in errors))

    def test_unknown_reusable_workflow_fails(self) -> None:
        bad = "uses: theapotheosisgroup/.github/.github/workflows/does-not-exist.yml@main\n"
        self.write("ok", bad, {"name": "OK", "description": "d"})
        self.assertTrue(any("does not exist" in e for e in check(self.dir)))

    def test_template_without_org_call_fails(self) -> None:
        self.write("ok", "jobs: {}\n", {"name": "OK", "description": "d"})
        self.assertTrue(any("does not call" in e for e in check(self.dir)))


if __name__ == "__main__":
    unittest.main()
