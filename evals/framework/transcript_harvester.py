#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PostToolUse hook that appends session transcripts to evals/transcripts/.

Wire into Claude Code settings.json:

    {
      "hooks": {
        "PostToolUse": [{
          "matcher": "*",
          "hooks": [{
            "type": "command",
            "command": "uv run /path/to/skills/evals/framework/transcript_harvester.py"
          }]
        }]
      }
    }

Claude Code feeds hook events as JSON on stdin. This script appends them
to a per-session JSONL file that later tooling can convert into locked-in
regression cases.

Stub implementation — writes raw events. A smarter version would normalize
into an eval-ready shape (input prompt + expected tool calls + final output).
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

TRANSCRIPTS_DIR = Path(__file__).resolve().parents[1] / "transcripts"


def main() -> int:
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    raw = sys.stdin.read()
    if not raw.strip():
        return 0

    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        event = {"raw": raw}

    event["_harvested_at"] = datetime.now(UTC).isoformat()

    session_id = event.get("session_id") or "unknown"
    outfile = TRANSCRIPTS_DIR / f"{session_id}.jsonl"

    with outfile.open("a") as f:
        f.write(json.dumps(event) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
