#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Validate SKILL.md frontmatter and required sections.

Enforces the Nothing Fancy quality bar on every plugins/*/skills/*/SKILL.md:
- Has YAML frontmatter with `name` and `description`.
- `name` is kebab-case, ≤64 chars, matches the parent directory.
- Body contains `## When to Use` and `## When NOT to Use` sections.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end].strip()
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None, text
    body = text[end + 4 :].lstrip()
    return data, body


def validate_skill(skill_md: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    rel = skill_md.relative_to(repo_root)
    text = skill_md.read_text()

    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None or not isinstance(frontmatter, dict):
        errors.append(f"{rel}: missing or invalid YAML frontmatter")
        return errors

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not name:
        errors.append(f"{rel}: frontmatter missing 'name'")
    else:
        if len(name) > 64:
            errors.append(f"{rel}: name '{name}' exceeds 64 chars")
        if not KEBAB_CASE.match(name):
            errors.append(f"{rel}: name '{name}' is not kebab-case")
        parent = skill_md.parent.name
        if name != parent:
            errors.append(
                f"{rel}: frontmatter name '{name}' does not match parent directory '{parent}'"
            )

    if not description:
        errors.append(f"{rel}: frontmatter missing 'description'")
    elif len(description) < 40:
        errors.append(
            f"{rel}: description is only {len(description)} chars — "
            f"add concrete triggers (minimum 40 chars)"
        )

    if "## When to Use" not in body:
        errors.append(f"{rel}: missing required section '## When to Use'")
    if "## When NOT to Use" not in body:
        errors.append(f"{rel}: missing required section '## When NOT to Use'")

    return errors


def main() -> int:
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent.parent
    plugins_dir = repo_root / "plugins"

    skill_files = sorted(plugins_dir.glob("*/skills/*/SKILL.md"))
    if not skill_files:
        print(f"No SKILL.md files found under {plugins_dir}")
        return 0

    all_errors: list[str] = []
    for skill_md in skill_files:
        all_errors.extend(validate_skill(skill_md, repo_root))

    if all_errors:
        print(f"Found {len(all_errors)} error(s):\n", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_files)} SKILL.md file(s) successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
