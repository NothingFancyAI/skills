#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml>=6.0",
#     "click>=8.1",
# ]
# ///
"""Nothing Fancy eval runner.

Thin wrapper over promptfoo that handles:
- Per-skill case discovery (evals/cases/<skill>/cases.yaml)
- Provider filtering (harness × model grid)
- Report rendering to evals/reports/

Stub implementation. The real runner shells out to `promptfoo eval` with
the right flags; this file establishes the CLI surface so cases can be
authored against a stable contract.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
EVALS_DIR = REPO_ROOT / "evals"
CASES_DIR = EVALS_DIR / "cases"
REPORTS_DIR = EVALS_DIR / "reports"
CONFIG_PATH = EVALS_DIR / "framework" / "promptfoo.config.yaml"


def discover_skills() -> list[str]:
    if not CASES_DIR.is_dir():
        return []
    return sorted(p.name for p in CASES_DIR.iterdir() if p.is_dir())


def load_cases(skill: str) -> dict:
    cases_path = CASES_DIR / skill / "cases.yaml"
    if not cases_path.exists():
        raise click.ClickException(f"No cases.yaml for skill '{skill}' at {cases_path}")
    return yaml.safe_load(cases_path.read_text())


@click.command()
@click.option("--skill", help="Run cases for a single skill only.")
@click.option("--provider", help="Filter to a single provider (e.g., anthropic:claude-sonnet-4-6).")
@click.option("--list-skills", is_flag=True, help="List discoverable skills and exit.")
@click.option("--dry-run", is_flag=True, help="Show what would run without invoking promptfoo.")
def main(skill: str | None, provider: str | None, list_skills: bool, dry_run: bool) -> None:
    """Run Nothing Fancy eval suites."""
    if list_skills:
        for s in discover_skills():
            click.echo(s)
        return

    skills = [skill] if skill else discover_skills()
    if not skills:
        raise click.ClickException(
            f"No skills found under {CASES_DIR}. Add cases.yaml files under evals/cases/<skill>/."
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    for s in skills:
        cases = load_cases(s)
        count = len(cases.get("tests", []))
        click.echo(f"skill={s} cases={count}" + (f" provider={provider}" if provider else ""))

        if dry_run:
            continue

        cmd = [
            "npx",
            "promptfoo",
            "eval",
            "--config",
            str(CONFIG_PATH),
            "--tests",
            str(CASES_DIR / s / "cases.yaml"),
            "--output",
            str(REPORTS_DIR / f"{s}.json"),
        ]
        if provider:
            cmd.extend(["--filter-providers", provider])

        click.echo("  " + " ".join(cmd))
        try:
            subprocess.run(cmd, check=True)
        except FileNotFoundError:
            click.echo(
                "  promptfoo not installed. Install with: npm install -g promptfoo",
                err=True,
            )
            sys.exit(1)
        except subprocess.CalledProcessError as exc:
            click.echo(f"  promptfoo exited {exc.returncode}", err=True)
            sys.exit(exc.returncode)


if __name__ == "__main__":
    main()
