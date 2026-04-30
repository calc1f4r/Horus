# Deepening Guide

Use this guide after identifying a cluster of shallow modules. The goal is to move behavior behind a stronger interface without exposing internal seams just for tests.

## Dependency categories

Classify dependencies before recommending a deepened module. The category determines where the seam belongs and how the module should be tested.

### 1. In-process

Pure computation or in-memory state with no I/O.

Recommendation: merge behavior behind a single interface and test through that interface directly. No adapter is needed.

### 2. Local-substitutable

Dependencies with realistic local stand-ins, such as an in-memory filesystem, SQLite/PGLite, fake clock, or local queue.

Recommendation: keep the dependency as an internal implementation detail and test the deep module with the local stand-in. Do not expose an external port only for tests.

### 3. Remote but owned

Networked dependencies owned by the same organization, such as internal HTTP services, RPC services, queues, or workers.

Recommendation: define a port at the seam. Put domain logic in the deep module. Use a production adapter for transport and an in-memory adapter for tests.

### 4. True external

Third-party services, payment providers, vendor APIs, external chains, and systems the project does not control.

Recommendation: inject a port at the seam and use a mock or fake adapter in tests. Keep vendor-specific behavior inside the production adapter or a vendor integration module.

## Seam discipline

- Do not introduce a port unless at least two adapters are justified, usually production plus test.
- A single-adapter seam is usually indirection, not depth.
- Deep modules can have internal seams, but internal seams should not leak through the external interface.
- The seam should be named in domain language when it represents a domain concept.

## Testing strategy

- Replace tests on shallow modules with tests at the deepened module's interface once equivalent behavior is covered.
- Tests should assert observable outcomes through the interface.
- Tests should survive internal implementation refactors.
- If a test must reach through the interface to assert internal state, the module shape is probably wrong.

## Recommendation shape

Use this form when proposing a dependency-aware deepening:

```md
Define a <domain-name> module with <interface summary>. Keep <dependency> behind <internal seam or port>. Production uses <adapter>. Tests use <stand-in or adapter>. This concentrates <behavior> in one implementation while preserving <caller benefit>.
```
