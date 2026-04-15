# Maintenance Mode

Specs and code both exist. The task is to keep the bidirectional graph current as the system evolves.

## Goal

Keep the graph healthy: specs point to implementing code, code points back to governing specs, divergence is surfaced explicitly.

## Operations

### 1. Audit

**When:** After a significant development cycle, before a release, or when onboarding new contributors.

Identify drift between specs and code:

1. **Enumerate specs** — List all spec files and their status fields.
2. **Enumerate code modules** — List all significant packages/modules.
3. **Cross-reference** — For each spec, verify:

   | Check | How | Drift Signal |
   |---|---|---|
   | Code exists | Follow code map links | Link target missing or renamed |
   | Code matches spec | Read code, compare to spec entities/APIs | Fields added/removed, endpoints changed |
   | Status is accurate | Compare spec status to implementation | Spec says "Planned" but code exists |

4. **Find orphan code** — Modules with no corresponding spec. Is this a spec gap, internal infrastructure, or dead code?
5. **Find orphan specs** — Specs whose code has been deleted. Intentional deprecation or accidental?

Produce a drift report with severity ratings. Report findings before making changes — let the developer decide whether spec or code is the source of truth for each discrepancy.

### 2. Update

**When:** After any code change that modifies public APIs, data models, configuration, or behavior documented in a spec.

**Code changed → update spec:**
1. Identify affected spec sections (new fields → entities, new endpoints → API, schema changes → storage).
2. Update sections to match current code.
3. Increment version, update date.
4. Update code map if file paths changed.
5. Add implementation notes for non-obvious changes.

**Spec changed → update code:**
1. Mark affected sections: `### 3.2 Session Entity (**PENDING IMPLEMENTATION**)`.
2. Create implementation tasks from the delta.
3. After implementation, remove the marker and update status.

**Rename/move operations:**
1. Search all specs for references to the old path.
2. Update code map tables and inline file references.

### 3. Extend

**When:** A new subsystem, feature, or integration is added.

1. Determine spec level: spans multiple packages → system; single endpoint → feature; cross-cutting → application-level update.
2. For system-level specs, run the full elicitation from existing-codebase mode.
3. For feature-level specs, run an abbreviated elicitation (Round 1 only).
4. Draft with explicit code mapping.
5. Add back-links from code to spec.

**Back-link convention:**
```
// Spec: specs/{system}-system.md#{section}
```

### 4. Prune

**When:** Code is removed, a feature is deprecated, or a subsystem is replaced.

**Deprecation** (code removed, spec kept for history):
```markdown
**Status:** Deprecated
**Deprecated:** YYYY-MM-DD
**Reason:** Replaced by {new-system-spec.md}
```

**Deletion** — only when the system was never implemented or the deprecated version adds no historical value. In most cases, deprecate rather than delete.

**Consolidation** — when multiple small specs should merge: create the consolidated spec, mark old specs as deprecated with a pointer, update the index.

## Maintenance cadence

| Trigger | Operation | Scope |
|---|---|---|
| PR merged with API changes | Update | Affected specs only |
| New package/module created | Extend | New spec for the module |
| Code deleted | Prune | Deprecate affected specs |
| Sprint/cycle boundary | Audit | Full spec set |
| Major refactor | Audit + Update | All affected specs |
| New team member onboarding | Audit | Verify coverage and accuracy |

## Socratic prompts for maintenance

When drift is ambiguous, ask:
- Which spec currently owns this behavior?
- Which code paths are now authoritative?
- What changed: intent, implementation, or both?
- Is this drift temporary, accidental, or the new target design?
- What proof of alignment exists: tests, endpoints, schemas, examples?
