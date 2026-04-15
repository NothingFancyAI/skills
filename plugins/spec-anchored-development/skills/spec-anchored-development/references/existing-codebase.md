# Existing-Codebase Mode

Code exists but specs are partial or missing. The task is to derive a coherent spec set without fabricating requirements.

## Goal

Move from implementation fragments to an explicit system map. Code tells you *what*; elicitation captures *why* and *what it should become*.

## Process

### 1. Survey the codebase, write the survey artifact

Before drafting any spec, produce `specs/_survey.md`. It captures what you observed so the rest of the run is grounded in facts, not re-discovery on every spec, and it has lasting value as a starting point for future maintenance runs and contributor onboarding. Treat it as **durable** — keep it across runs and update it during maintenance when the topology changes substantially.

Map and record:
- Package/module structure and dependency graph
- Public API surfaces (HTTP routes, exported functions, CLI commands)
- Data models and persistence (DB schemas, file formats, state)
- Configuration and environment variables
- Entry points and bootstrap chain
- **Seam files** — files that obviously straddle two systems (entry points, plugin wiring, route registration, event bus). These will need scoped multi-link back-links.
- **Cross-cutting concerns** — concepts referenced from many places but owned by no single module (event format, identity scheme, naming conventions). Candidates for cross-cutting specs.

### 2. Identify systems

Group related code into logical systems by domain, not by directory. Each system with its own data model, API surface, or lifecycle is a candidate for a spec. Reserve cross-cutting specs for the concerns surfaced in step 1; do not invent them.

Present the proposed breakdown to the developer for validation. Include the proposed spec id for each system (the value that will go into `spec:` frontmatter) since back-links will use that id, not the filename.

### 3. For each system: extract then interview

The interview rounds map directly onto the required sections in SKILL.md. Ask only what the code cannot tell you; do not waste cycles re-discovering observable facts.

**Extract from code first (what you can observe):**
- Data models (types, structs, schemas) — paste the real types into the Core entities section
- API surface (routes, endpoints, CLI commands)
- Database schema (migrations, table definitions)
- State machines (status enums, transition logic)
- Dependencies and integration points
- Error types and handling patterns
- Tests covering the system — these become the Test map

**Then ask the developer (what code can't tell you):**

#### Round 1: Why and tradeoffs

Targets the **Why** and **Tradeoffs** sections. These are the two highest-value pieces of intent and the hardest to recover later.

| Ask | Purpose |
|---|---|
| Why does this system exist? What problem does it solve? | Why section |
| What would be easy to break by accident if someone edited this without context? | Why section — the hidden traps |
| What's the intended future direction? | Target design |
| What design decisions were made, and what alternatives were considered? | Tradeoffs section |
| Why were rejected alternatives rejected? | Tradeoffs section — prevents re-litigation |

#### Round 2: Invariants and boundaries

Targets the **Invariants**, **Goals & non-goals**, and **Failure modes** sections.

| Ask | Purpose |
|---|---|
| What invariants must always hold? Phrase them so they could be falsified. | Invariants |
| What's explicitly out of scope, and why? | Non-goals |
| What auth, privacy, or safety boundaries apply? | Invariants / non-goals |
| What failure modes exist and how are they handled? | Failure modes |
| What's fragile, tricky, or surprising about the implementation? | Edit impact (the "if you change X" entries) |

#### Round 3: Edit coupling and verification

Targets the **Edit impact** and **Test map** sections. This is where you elicit the cross-system coupling that prevents future edits from breaking adjacent systems.

| Ask | Purpose |
|---|---|
| When you change behavior in this system, what other files do you always end up editing too? | Edit impact entries |
| When this system breaks, what's the first thing that surfaces the failure? Tests, logs, alerts? | Failure modes / Test map |
| What tests prove the invariants you named in Round 2? | Test map |
| What external dependencies matter, and what are the assumptions you make about them? | Failure modes |

#### Round 4: Status and known deltas

Targets the **status** field and **Known deltas** section.

| Ask | Purpose |
|---|---|
| Does the code currently match the design you just described? | Set status: `current` or `drifted` |
| If not, where does it diverge? | Known deltas entries |
| Are any parts aspirational or in flight? | Known deltas / `implementation` status |

### Interview style

Ground every question in specific code you've read. Point at code and ask *why*:

> "I see `SessionManager` handles both creation and cleanup. Was this intentional coupling, or would these be better separate?"

> "`MonitorStatus` has four states. Is 'Paused' user-initiated or system-initiated? What triggers Late → Down?"

Avoid abstract questions ("tell me about the architecture"). Ask one question at a time.

### 4. Draft the spec

Combine extracted facts with stated intent. The code is authority for *what is*; the developer is authority for *what should be* and *why*.

Use the locked frontmatter schema and the required-sections list from SKILL.md. Every section must be present — empty placeholders are not allowed for Why, Invariants, Tradeoffs, or Edit Impact.

Separate observed current state from target design. If they differ, set status to `drifted` and record the divergence in Known deltas. Do not silently align the spec to the code or the code to the spec.

### 5. Build the bidirectional map

This step is not optional. Both directions must be created in the same pass.

**Spec → code (code map + test map in the spec):**
Add the Code map and Test map sections. Link spec sections to implementing files. Use symbol names (`AgentExecutor.run`) for stable anchors; line numbers may augment but should not stand alone.

**Code → spec (`Spec:` comments in code files):**
Add a `Spec:` comment to every owning file using the **spec id** from the target spec's frontmatter (not the filename). Section anchors are mandatory when scope is partial. Multi-link only on true seam files identified during the survey, with scope qualifiers on each line. See SKILL.md for the locked format.

### 6. Build the spec index and conventions file

After all specs in this run are drafted:

- Generate `SPEC_INDEX.md` from the frontmatter of every spec. Include the topology Mermaid.
- Write `specs/CONVENTIONS.md` if it does not exist. It distills the frontmatter schema, status enum, back-link format, and required sections so future PRs follow the same rules without this skill loaded.

### 7. Run the completion gates

Before reporting the run as done, run the gates from SKILL.md. Pay special attention to gate 1 (back-links exist) — this is the most common regression. Use the language-agnostic extractor: `grep -rEn '^(// |# )Spec:' <code-root>` (or `rg -n '^(//|#) Spec:' <code-root>`). If it returns zero matches for a non-`draft` system you wrote a spec for, the run is incomplete.

## Minimum output

1. `specs/_survey.md` (durable survey artifact from step 1)
2. `SPEC_INDEX.md` generated from frontmatter
3. `specs/CONVENTIONS.md` distilled from this skill
4. One architecture or system-map spec
5. One durable spec per cohesive domain, each with full required sections
6. `// Spec:` back-links in every owning code file
7. Optional migration or cleanup plan if the codebase is inconsistent
