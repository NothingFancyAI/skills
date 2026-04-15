# Maintenance Mode

Specs and code both exist. The task is to keep the bidirectional graph current as the system evolves. Maintenance is **diff-driven** — it operates on what changed since the last sync, not on the full repo.

## Goal

Keep the graph healthy: specs point to implementing code, code points back to governing specs, divergence is surfaced as `drifted` status with concrete deltas, never silently smoothed over.

## Inputs

A maintenance run takes a git range (e.g. `main..HEAD`, last release tag..HEAD, or a list of recently-changed files).

**Default when the user does not specify:** the working tree (uncommitted + staged) combined with `HEAD~1..HEAD`. This covers the common case of "I just made some edits and want them reflected in specs." Proceed with the default rather than blocking on clarification. Only ask for an explicit range if the working tree is clean *and* `HEAD~1..HEAD` shows nothing relevant to any spec's `owners`. State the chosen range in the run summary so the user can correct it if needed.

## Operations

### 1. Audit (drift detection)

**When:** After a development cycle, before a release, or as the first step of any maintenance run.

For every spec whose `owners` files appear in the diff, run these checks:

| Check | How | Drift signal |
|---|---|---|
| Owners files exist | Resolve every path in `owners` | Path missing or renamed |
| Owners files have back-links | Search the file for a `Spec:` comment using the language's prefix (`//` for TS/JS/Go, `#` for Python). Use the same extractor as in SKILL.md (Code-to-spec back-link format → Extraction) | Zero matches → missing back-link |
| Back-link spec id resolves | Look up the id in the spec index | Stale id (spec renamed/deleted) |
| Section anchors resolve | Match `#section` in the back-link against the spec's headings | Anchor missing or renamed |
| `last_updated` vs commit history | Compare to the most recent **semantic** commit on any `owners` file. **Exclude** comment-only edits, formatting/whitespace changes, test-only changes, and commits with conventional prefixes `style:`, `chore:`, `docs:`, `test:` | Stale `last_updated` → **informational only**, low severity. On its own this never escalates to `drifted`; it is a hint to re-read the spec, not a verdict |
| Core entities still match | Read entity definitions in the spec, diff against source types | Field added/removed, type changed |
| External surfaces match | Compare HTTP routes, CLI commands, exports | Route added/removed, signature changed |
| Status is consistent | A `current` spec with any of the above failing | Should be `drifted` |

Also check the inverse direction:

| Check | How | Drift signal |
|---|---|---|
| Renamed/moved files in specs | Search code map tables for paths that no longer exist | Stale code map entry |
| Orphan code | Owning files (core, routes, stateful, schema, UI state) with no back-link | Spec gap or missing back-link |
| Orphan specs | Specs whose `owners` files have all been deleted | Should be `deprecated` or removed |
| Index out of sync | `SPEC_INDEX.md` columns vs current frontmatter | Re-generate the index |

Produce a drift report. Severity:

- **High** — `current` specs that should be `drifted`; missing back-links; broken back-link ids
- **Medium** — stale code map paths; missing test map entries; index out of sync
- **Low (informational)** — `last_updated` stale but content still matches; never on its own a reason to mark a spec `drifted`

Report findings before making changes. Let the developer decide whether spec or code is the source of truth for each discrepancy.

### 2. Update

**When:** After any code change that modifies public APIs, data models, configuration, invariants, or behavior documented in a spec.

**Code changed → update spec:**

1. Identify affected sections (entity changes → Core entities; route changes → External surfaces; new failure path → Failure modes; new coupling → Edit impact).
2. Update sections to match current code, **pasting** the real types.
3. Bump `version` and `last_updated` in the frontmatter.
4. Update the Code map and Test map if file paths or symbols changed.
5. If invariants or tradeoffs changed, the change is significant — flag it for human review rather than silently editing.

**Spec changed → update code:**

1. Set spec status to `implementation` and add a Known deltas entry naming the gap.
2. Implement against the spec.
3. When code matches, set status back to `current` and clear the delta.

**Drift resolution (`current` spec → divergent code):**

1. Set status to `drifted`.
2. Add a Known deltas entry with: the divergence, the reason (if known), the owner, and a tracking link.
3. Decide direction with the developer:
   - If code is correct → update the spec, then set back to `current`.
   - If spec is correct → update the code, then set back to `current`.
   - If neither, leave `drifted` until decided. Do not invent a third option.

**Rename/move operations:**

1. Search all specs and `SPEC_INDEX.md` for references to the old path.
2. Update `owners`, code map tables, and test map entries.
3. Back-link comments use the spec **id**, not the filename, so spec renames do not cascade — but file renames inside `owners` do.

### 3. Extend

**When:** A new subsystem, feature, or integration is added.

1. Determine spec level: spans multiple packages → system; single endpoint → feature; concept shared across systems → cross-cutting; cross-cutting architecture → application-level update.
2. For system-level specs, run the full elicitation from existing-codebase mode.
3. For feature-level specs, run an abbreviated elicitation (Round 1 only).
4. Draft with the locked frontmatter and required sections.
5. Add `// Spec:` back-links to every owning file using the new spec's id.
6. Re-generate `SPEC_INDEX.md`.

**Back-link convention:**
```
// Spec: <spec-id>[#section] [— description]
```
Use the spec **id** from frontmatter, not the filename. See SKILL.md for the full format and rules on multi-link seam files.

### 4. Prune

**When:** Code is removed, a feature is deprecated, or a subsystem is replaced.

**Deprecation** (code removed, spec kept for history):
```yaml
---
status: deprecated
deprecated: 2026-04-14
replaced_by: new-system          # spec id of the replacement, if any
---
```
`deprecated` is sticky. New code must not reference deprecated specs; the audit flags any back-link from a file changed after the deprecation date.

**Deletion** — only when the system was never implemented or the deprecated version adds no historical value. In most cases, deprecate rather than delete.

**Consolidation** — when multiple small specs should merge: create the consolidated spec with a new id, mark old specs as `deprecated` with `replaced_by` pointing to the new id, update the index. Old back-links continue to resolve via the old ids until the next maintenance pass updates them.

## Maintenance cadence

| Trigger | Operation | Scope |
|---|---|---|
| PR merged with API or behavior changes | Update | Affected specs only |
| New package/module created | Extend | New spec for the module |
| Code deleted | Prune | Deprecate affected specs |
| Sprint/cycle boundary | Audit | Diff since last audit |
| Major refactor | Audit + Update | All specs whose owners changed |
| New team member onboarding | Audit | Read-only — verify coverage and accuracy |

## Socratic prompts for ambiguous drift

When drift is ambiguous, ask:
- Which spec currently owns this behavior?
- Which code paths are now authoritative?
- What changed: intent, implementation, or both?
- Is this drift temporary, accidental, or the new target design?
- What proof of alignment exists: tests, endpoints, schemas, examples?

## Run the completion gates

After any maintenance operation, run the gates from SKILL.md. Specifically:

- All touched specs have valid frontmatter and a status from the enum
- Every owning file has a back-link using the spec id
- `SPEC_INDEX.md` is regenerated if frontmatter changed
- The drift report is included in the run summary, even if all checks passed (so the user knows what was checked)
