#!/usr/bin/env python3
"""Check GitHub workflow templates and their .properties.json metadata.

GitHub lists a template only when ``workflow-templates/<name>.yml`` has a matching
``<name>.properties.json`` with a ``name`` and a ``description``. This script fails when a
template and its metadata do not pair up, when metadata is malformed, when an icon file is
missing, or when a template calls a reusable workflow that does not exist in this repository.

Usage: check_workflow_templates.py <templates-dir>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REUSABLE = re.compile(
    r"uses:\s*theapotheosisgroup/\.github/\.github/workflows/(?P<file>[A-Za-z0-9._-]+\.ya?ml)@"
)


def check(templates: Path) -> list[str]:
    errors: list[str] = []
    workflows = {p.stem: p for p in templates.glob("*.yml")} | {
        p.stem: p for p in templates.glob("*.yaml")
    }
    metadata = {
        p.name.removesuffix(".properties.json"): p
        for p in templates.glob("*.properties.json")
    }

    if not workflows:
        errors.append(f"{templates}: no workflow templates found")

    for stem in sorted(set(workflows) - set(metadata)):
        errors.append(f"{workflows[stem]}: missing {stem}.properties.json")
    for stem in sorted(set(metadata) - set(workflows)):
        errors.append(f"{metadata[stem]}: no matching {stem}.yml")

    for stem, path in sorted(metadata.items()):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{path}: top level must be an object")
            continue
        for key in ("name", "description"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                errors.append(f"{path}: '{key}' must be a non-empty string")
        unknown = set(data) - {
            "name",
            "description",
            "iconName",
            "categories",
            "filePatterns",
        }
        if unknown:
            errors.append(f"{path}: unknown keys {sorted(unknown)}")
        for key in ("categories", "filePatterns"):
            value = data.get(key, [])
            if not isinstance(value, list) or not all(
                isinstance(v, str) for v in value
            ):
                errors.append(f"{path}: '{key}' must be a list of strings")
        for pattern in (
            data.get("filePatterns", [])
            if isinstance(data.get("filePatterns"), list)
            else []
        ):
            try:
                re.compile(pattern)
            except re.error as exc:
                errors.append(
                    f"{path}: filePatterns entry {pattern!r} is not a valid regex: {exc}"
                )
        icon = data.get("iconName")
        if icon is not None:
            if not isinstance(icon, str) or not icon.strip():
                errors.append(f"{path}: 'iconName' must be a non-empty string")
            elif (
                not icon.startswith("octicon ")
                and not (templates / f"{icon}.svg").is_file()
            ):
                errors.append(
                    f"{path}: iconName {icon!r} has no {icon}.svg in {templates}"
                )

    for stem, path in sorted(workflows.items()):
        text = path.read_text(encoding="utf-8")
        called = REUSABLE.findall(text)
        if not called:
            errors.append(f"{path}: does not call an organization reusable workflow")
        for name in called:
            if not (REPO_ROOT / ".github" / "workflows" / name).is_file():
                errors.append(
                    f"{path}: calls .github/workflows/{name}, which does not exist"
                )
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    errors = check(Path(argv[1]))
    for error in errors:
        print(f"error: {error}")
    if errors:
        return 1
    print("workflow templates: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
