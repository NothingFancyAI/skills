# TypeScript Guidance

Use TypeScript-native anchors across backend, frontend, or full-stack repos.

## Architecture anchors

- package boundaries in monorepos or apps
- runtime surfaces: Node services, browser clients, SSR apps, workers, CLIs
- build and generation boundaries such as Vite, Next.js, tsup, or shared schema packages

## Native forms to show in specs

- `type`, `interface`, discriminated unions, branded identifiers, and schema validators
- request and event payloads
- runtime validation boundaries using tools such as Zod, Valibot, or custom guards
- persistence ownership and generated client boundaries

## Questions to force clarity

- Which types are compile-time only and which are runtime-enforced?
- Where are shared contracts published and versioned?
- How do browser, server, and worker boundaries differ?
- What state is local, cached, persisted, or synchronized?
- What tests prove behavior across type and runtime boundaries?

## Traceability examples

- spec -> `packages/*`, `apps/*`, `src/server/`, `src/lib/`, `src/routes/`
- spec -> `openapi/`, `prisma/`, `migrations/`, `workers/`
- code breadcrumb -> package README, file header, route module comment, or generated doc index already used by the repo
