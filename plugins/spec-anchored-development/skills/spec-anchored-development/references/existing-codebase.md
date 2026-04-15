# Existing-Codebase Mode

Code exists but specs are partial or missing. The task is to derive a coherent spec set without fabricating requirements.

## Goal

Move from implementation fragments to an explicit system map. Code tells you *what*; elicitation captures *why* and *what it should become*.

## Process

### 1. Survey the codebase

Map the top-level structure before asking any questions:
- Package/module structure and dependency graph
- Public API surfaces (HTTP routes, exported functions, CLI commands)
- Data models and persistence (DB schemas, file formats, state)
- Configuration and environment variables
- Entry points and bootstrap chain

### 2. Identify systems

Group related code into logical systems by domain, not by directory. Each system with its own data model, API surface, or lifecycle is a candidate for a spec. Present the proposed breakdown to the developer for validation.

### 3. For each system: extract then interview

**Extract from code first (what you can observe):**
- Data models (types, structs, schemas)
- API surface (routes, endpoints, CLI commands)
- Database schema (migrations, table definitions)
- State machines (status enums, transition logic)
- Dependencies and integration points
- Error types and handling patterns

**Then ask the developer (what code can't tell you):**

#### Round 1: System framing

| Ask | Purpose |
|---|---|
| Why does this system exist? What problem does it solve? | Core intent |
| What are the goals and non-goals? | Boundaries |
| What design decisions were made and why? | Rationale |
| What trade-offs were accepted? | Constraints |
| What's the intended future direction? | Target design |

#### Round 2: Ownership and invariants

| Ask | Purpose |
|---|---|
| What invariants must always hold? | Safety properties |
| What's fragile, tricky, or surprising? | Risk areas |
| What parts are stable vs accidental? | Spec confidence |
| What auth, privacy, or safety boundaries apply? | Security scope |

#### Round 3: Operational reality

| Ask | Purpose |
|---|---|
| What failure modes or retries exist? | Resilience |
| What tests or runtime signals prove correctness? | Verification |
| What external dependencies matter? | Coupling |

### Interview style

Ground every question in specific code you've read. Point at code and ask *why*:

> "I see `SessionManager` handles both creation and cleanup. Was this intentional coupling, or would these be better separate?"

> "`MonitorStatus` has four states. Is 'Paused' user-initiated or system-initiated? What triggers Late → Down?"

Avoid abstract questions ("tell me about the architecture"). Ask one question at a time.

### 4. Draft the spec

Combine extracted facts with stated intent. The code is authority for *what is*; the developer is authority for *what should be* and *why*.

Separate observed current state from target design when they differ. Record unknowns as open questions instead of guessing.

### 5. Build the bidirectional map

This step is not optional. Both directions must be created in the same pass.

**Spec → code (code map table in the spec):**
Add a mapping table at the end of each spec linking sections to implementing files.

**Code → spec (`Spec:` comments in code files):**
Add a `Spec:` comment to every significant implementing file. Use the format defined in SKILL.md. Include a description when the file only implements part of a spec or when scope/intent needs clarification. Files at system boundaries may reference multiple specs.

## Minimum output

1. Spec index for the recovered set
2. One architecture or system-map spec
3. One durable spec per cohesive domain
4. Optional migration or cleanup plan if the codebase is inconsistent
