# Evals

Evals are the quality bar for this marketplace. A skill without evals is an untested skill, and untested skills don't graduate to public distribution.

## The pitch

Model jaggedness is real. The same prompt runs differently on Claude Sonnet 4.6, Opus 4.6, GPT-5-Codex, Haiku 4.5, and pi's default. Skills that look great in one harness can silently misfire in another.

The honest way to answer "is this skill good?" is to run it across the grid and measure. That's what this framework is for.

**Evals in this repo are not just regression tests.** They are **cross-harness comparison suites**:

- **Axis 1 — harness**: Claude Code, Codex, pi.
- **Axis 2 — model**: whichever models the harness supports.
- **Axis 3 — scenario**: positive trigger, negative trigger (must NOT fire), adversarial edge case.

A passing eval is one where every (harness × model × scenario) cell matches expectations. A *useful* eval run reports the cells where the grid diverges — that's where model or harness choice actually matters.

This is the cornerstone of the Nothing Fancy approach: we don't pick favorites; we measure.

## Layout

```
evals/
├── README.md                         # this file
├── framework/
│   ├── run.py                        # entrypoint: `uv run evals/framework/run.py`
│   ├── transcript_harvester.py       # PostToolUse hook → JSONL transcripts
│   └── promptfoo.config.yaml         # root promptfoo config (providers × assertions)
├── cases/
│   └── <skill-name>/
│       └── cases.yaml                # promptfoo test cases for this skill
├── transcripts/                      # harvested session logs (gitignored)
└── reports/                          # rendered run reports (gitignored)
```

## Required cases per skill

Every skill must ship at least three cases:

1. **Positive** — a realistic user prompt that SHOULD fire the skill. Assert that the skill's guidance is followed.
2. **Negative** — a prompt that looks related but should NOT fire the skill. Assert it isn't invoked.
3. **Edge** — an adversarial or historically-broken input, locked in as a regression.

Additional cases are encouraged, especially for surfaces where the skill makes judgment calls.

## Running

### Local single-skill run

```sh
uv run evals/framework/run.py --skill justfile
```

### Full suite (all skills, all providers)

```sh
uv run evals/framework/run.py
```

### Single-provider run (faster iteration)

```sh
uv run evals/framework/run.py --skill justfile --provider claude-sonnet-4-6
```

## Providers

Configured in `framework/promptfoo.config.yaml`. Currently stubbed for:

- `anthropic:claude-opus-4-6`
- `anthropic:claude-sonnet-4-6`
- `anthropic:claude-haiku-4-5`
- `openai:gpt-5-codex` (via Codex harness adapter)
- `pi:default` (via pi harness adapter)

Adapters for Codex and pi are stubs — the API-only Anthropic provider works out of the box. Filling in the harness-adapter providers is tracked as work-in-progress.

## Transcript harvesting

For in-the-wild data, `transcript_harvester.py` is a PostToolUse hook stub that dumps session JSONL to `evals/transcripts/`. Wire it into Claude Code's hooks to collect real usage, then convert notable failures into locked-in regression cases via:

```sh
uv run evals/framework/run.py --import-transcript evals/transcripts/<file>.jsonl
```

(Not yet implemented — stub in place.)

## Future directions

- **gepa integration.** Genetic-evolutionary prompt adaptation — mutate skill body text against eval scores as the fitness function. Useful once we have enough transcripts and cases to define a meaningful gradient. For now, a one-paragraph note; scaffolding deferred.
- **CI gate.** Block PRs whose eval scores regress below the previous release baseline. Needs a baseline artifact format first.
- **Cross-run diffing.** When a skill body changes, report which (harness × model × scenario) cells shifted — not just the aggregate pass rate. The interesting signal is *where* a change helps and hurts.

## References

- [promptfoo documentation](https://www.promptfoo.dev/docs/intro)
- [Agent Skills spec](https://agentskills.io/specification) — what we're actually testing
- [Model jaggedness](https://arxiv.org/abs/2406.04604) — background on why the grid matters
