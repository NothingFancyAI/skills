# Python Guidance

Use Python-native anchors in specs instead of generic pseudocode.

## Architecture anchors

- Package and module layout
- Service boundaries, background workers, and entrypoints
- Framework surfaces such as FastAPI, Django, Flask, Click, Typer, Celery, or asyncio services

## Native forms to show in specs

- `dataclass`, `TypedDict`, `Protocol`, `Enum`, and Pydantic models where relevant
- function and method signatures with type hints
- settings objects and environment variables
- migration ownership for ORMs such as SQLAlchemy, Django ORM, or Alembic

## Questions to force clarity

- Which package owns the domain model versus transport schema?
- Are contracts runtime-validated, type-checked, or both?
- Which async boundaries exist and where does concurrency matter?
- What settings are required per environment?
- Which tests prove invariants: unit, integration, contract, property, end-to-end?

## Traceability examples

- spec -> `src/package/subsystem/`
- spec -> `app/api/routes.py`
- spec -> `package/services/`, `package/models/`, `tests/`
- code back-link -> `# Spec:` comment per the [canonical back-link format](../SKILL.md#code-to-spec-back-link-format); for package-level ownership, place it in `__init__.py`
