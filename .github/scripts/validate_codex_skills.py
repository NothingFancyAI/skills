#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Validate that every plugin skill has a matching Codex sidecar entry.

Checks that for every plugins/<plugin>/skills/<skill>/SKILL.md there is
a corresponding .codex/skills/<skill>/ that either:
- is a symlink resolving to the plugin skill directory, or
- contains its own SKILL.md (for Codex-only skills).

Adapted from Trail of Bits' validate_codex_skills.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_DIR = REPO_ROOT / "plugins"
CODEX_SKILLS_DIR = REPO_ROOT / ".codex" / "skills"


def plugin_skill_dirs() -> dict[str, Path]:
    if not PLUGINS_DIR.is_dir():
        raise SystemExit(f"Plugins directory not found: {PLUGINS_DIR}")
    mapping: dict[str, Path] = {}
    for skill_md in sorted(PLUGINS_DIR.glob("*/skills/*/SKILL.md")):
        skill_dir = skill_md.parent
        name = skill_dir.name
        if name in mapping:
            raise SystemExit(f"Duplicate skill name '{name}' at {mapping[name]} and {skill_dir}")
        mapping[name] = skill_dir
    return mapping


def codex_skill_entries() -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    if not CODEX_SKILLS_DIR.exists():
        return mapping
    for entry in sorted(CODEX_SKILLS_DIR.iterdir()):
        mapping[entry.name] = entry
    return mapping


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    plugin_skills = plugin_skill_dirs()
    codex_entries = codex_skill_entries()
    errors: list[str] = []

    if not CODEX_SKILLS_DIR.exists():
        print(
            ".codex/skills/ does not exist — create it with symlinks to plugin skills",
            file=sys.stderr,
        )
        return 1

    for name, skill_dir in plugin_skills.items():
        codex_entry = codex_entries.get(name)
        if codex_entry is None:
            errors.append(
                f"Missing Codex sidecar for skill '{name}'. "
                f"Create with: ln -sfn ../../{rel(skill_dir)} .codex/skills/{name}"
            )
            continue

        if codex_entry.is_symlink():
            resolved = codex_entry.resolve()
            if not resolved.exists():
                errors.append(f"Dangling symlink for '{name}': {rel(codex_entry)} -> {resolved}")
            elif resolved != skill_dir.resolve():
                errors.append(
                    f"Mismatched Codex symlink for '{name}': "
                    f"{rel(codex_entry)} -> {resolved}, expected {skill_dir.resolve()}"
                )
        else:
            skill_md = codex_entry / "SKILL.md"
            if not skill_md.exists():
                errors.append(
                    f"Codex entry '{name}' is not a symlink and has no SKILL.md at {rel(skill_md)}"
                )

    for name, codex_entry in codex_entries.items():
        if name in plugin_skills:
            continue
        skill_md = codex_entry / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"Codex-only entry '{name}' must contain SKILL.md at {rel(skill_md)}")

    if errors:
        print("Codex skill validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(plugin_skills)} plugin skills against "
        f"{len(codex_entries)} Codex entries successfully"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
