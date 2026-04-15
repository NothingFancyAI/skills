# Go Guidance

Use Go-native anchors and ownership boundaries.

## Architecture anchors

- module and package layout
- command entrypoints under `cmd/`
- internal versus public packages
- transport layers such as HTTP, gRPC, workers, or CLIs

## Native forms to show in specs

- `struct`, `interface`, and typed error patterns
- context propagation boundaries
- configuration structs and environment contract
- storage and migration ownership

## Questions to force clarity

- Which package owns the domain logic versus adapters?
- What belongs in `internal/` versus exported packages?
- Where are interfaces actually needed instead of being speculative abstractions?
- How are cancellation, deadlines, retries, and idempotency handled?
- What observability contracts exist for logs, metrics, tracing, and health?

## Traceability examples

- spec -> `cmd/api/`, `internal/service/`, `internal/store/`
- spec -> `pkg/client/` when there is a supported library surface
- spec -> `migrations/`, `api/`, `test/`
- code breadcrumb -> package comment, doc.go, or nearby design README
