#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Report plugin, skill, and eval-case counts across the marketplace.

Run via `just stats`. Output is human-readable summary plus per-plugin
detail, flagging skills without eval coverage.

Exit 0 regardless of coverage gaps — this is informational, not a gate.
If you want coverage enforcement, call from CI with additional logic.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_DIR = REPO_ROOT / "plugins"
CASES_DIR = REPO_ROOT / "evals" / "cases"


def count_cases(skill_name: str) -> int | None:
    cases_path = CASES_DIR / skill_name / "cases.yaml"
    if not cases_path.exists():
        return None
    try:
        data = yaml.safe_load(cases_path.read_text())
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    tests = data.get("tests") or []
    return len(tests)


def discover_skills() -> list[tuple[str, str]]:
    """Return (plugin_name, skill_name) pairs for every SKILL.md found."""
    pairs: list[tuple[str, str]] = []
    for skill_md in sorted(PLUGINS_DIR.glob("*/skills/*/SKILL.md")):
        skill_name = skill_md.parent.name
        plugin_name = skill_md.parent.parent.parent.name
        pairs.append((plugin_name, skill_name))
    return pairs


def main() -> int:
    if not PLUGINS_DIR.is_dir():
        print(f"No plugins directory at {PLUGINS_DIR}", file=sys.stderr)
        return 0

    plugins = sorted(p.name for p in PLUGINS_DIR.iterdir() if p.is_dir())
    skills = discover_skills()

    total_plugins = len(plugins)
    total_skills = len(skills)
    total_cases = 0
    covered_skills = 0
    rows: list[tuple[str, str, int | None]] = []

    for plugin_name, skill_name in skills:
        cases = count_cases(skill_name)
        rows.append((plugin_name, skill_name, cases))
        if cases is not None:
            total_cases += cases
            covered_skills += 1

    print("Nothing Fancy skills — stats")
    print("─" * 44)
    print(f"Plugins:     {total_plugins}")
    print(f"Skills:      {total_skills}")
    print(f"Eval cases:  {total_cases}")
    print(f"Coverage:    {covered_skills}/{total_skills} skills have cases")
    print()
    print("Per-skill breakdown:")

    if not rows:
        print("  (no skills yet)")
        return 0

    max_skill = max(len(s) for _, s, _ in rows)

    for plugin_name, skill_name, cases in rows:
        mark = "✓" if cases else "✗"
        cases_str = f"{cases} cases" if cases else "MISSING"
        suffix = ""
        if plugin_name != skill_name:
            suffix = f"  (in plugin {plugin_name})"
        print(f"  {mark} {skill_name.ljust(max_skill)}  {cases_str}{suffix}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
