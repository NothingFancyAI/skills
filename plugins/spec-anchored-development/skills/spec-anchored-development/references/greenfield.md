# Greenfield Mode

The project is new or the user wants a baseline spec set before substantial code exists.

## Goal

Create the smallest useful spec set that can steer implementation and stay maintainable.

## Process

Do NOT generate the spec immediately. Guide the conversation through progressive Socratic phases. Ask 3-5 questions per round. Wait for answers before proceeding. Paraphrase answers back to confirm understanding before moving on.

### Round 1: Domain understanding

Understand the problem space before any design.

| Ask | Purpose |
|---|---|
| What problem does this system solve? | Core value proposition |
| Who are the users or consumers? | Audience |
| What existing systems inspire this? | Prior art and expectations |
| What does success look like? | Acceptance criteria |
| What failure modes concern you most? | Risk surface |

Follow-up probes:
- "Walk me through a concrete scenario of how a user interacts with this."
- "What's the single most important use case?"
- "What would make this a failure even if it technically works?"

### Round 2: Scope definition

Draw clear boundaries.

| Ask | Purpose |
|---|---|
| Must-have features for v1? | Define MVP |
| What's explicitly deferred? | Non-goals |
| What existing systems does this integrate with? | Dependencies |
| Hard constraints (performance, security, compliance)? | Requirements |
| What is the deployment target? | Runtime context |

Follow-up probes:
- "If you cut one feature, which one?"
- "What's the riskiest part?"
- "Is there a hard deadline driving the scope?"

### Round 3: Entity modeling

Define core data structures and relationships.

| Ask | Purpose |
|---|---|
| Primary entities or resources? | Domain objects |
| Essential fields for each? | Schema |
| How do entities relate? | Relationships |
| State machines or lifecycles? | Workflows |
| How is each entity identified? | Identity model |

Follow-up probes:
- "Does this entity belong to a user, org, or is it global?"
- "What happens when the owner is deleted?"
- "What state transitions are allowed, and what triggers them?"
- "Are there terminal states?"

### Round 4: Technical decisions

Make architecture explicit.

| Ask | Purpose |
|---|---|
| Package/module structure? | Code organization |
| What patterns from similar systems apply? | Consistency |
| Authentication/authorization model? | Security |
| API surface (REST, gRPC, CLI, WebSocket)? | Interface design |
| Storage strategy? | Persistence |

Follow-up probes:
- "Should clients poll or should the server push?"
- "What happens if [component] is unavailable?"
- "Eventual consistency acceptable, or strong consistency required?"

### Round 5: Implementation planning

Create actionable phases.

| Ask | Purpose |
|---|---|
| Logical implementation order? | Dependencies |
| What can be built in parallel? | Parallelism |
| Integration points? | Touch points |
| Testing requirements? | Quality gates |
| Smallest deployable subset? | Incremental delivery |

Follow-up probes:
- "What existing tests need updating?"
- "What monitoring is needed at launch?"

## After the interview

1. Draft the spec using the locked frontmatter and required-sections list from SKILL.md. Initial status is `draft`. Code map and Test map start empty; populate them as code lands. Known deltas starts empty.
2. The Why section should reflect Round 1 answers; Tradeoffs from Round 4 alternatives discussed; Invariants from Round 2 hard constraints. Edit impact uses the explicit placeholder `_(none yet — populate when the system grows or status reaches current)_` until the system spans more than one module.
3. Run the quality checklist from SKILL.md (status enum aside — `draft` specs cannot fail the back-link gate yet).
4. Run the refinement loop:
   - **Completeness**: Have all relevant sections been addressed?
   - **Consistency**: Does this align with existing code and spec patterns?
   - **Clarity**: Could a new developer implement this without further questions?
   - **Edge cases**: What happens with empty inputs, concurrent access, partial failures?

## Minimum output

1. `SPEC_INDEX.md` with domain grouping and intended code homes
2. `specs/CONVENTIONS.md` distilled from SKILL.md
3. Architecture spec with boundaries and data flow
4. Initial domain specs (status: `draft`) with all required sections — the Why, Invariants, Tradeoffs, Goals & non-goals, and Core entities are the load-bearing ones at this stage
5. Optional implementation plan for the first delivery slice

When code starts landing, transition specs to `implementation` and add back-links and code/test map entries as they become real.
