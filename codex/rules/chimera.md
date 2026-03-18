<!-- AUTO-GENERATED from `.claude/rules/chimera.md`; source_sha256=2c034e8136b4fd368188d4747e2aab7bc0cc4b702ece0917a7b39f04d21512cc -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/chimera.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "test/recon/**"
  - "test/recon/*.sol"
  - "test/recon/targets/*.sol"
---

# Chimera Rules

When working with files in `test/recon/`:

## Contract Hierarchy

```
BaseSetup → BaseProperties → BaseTargetFunctions (+ Asserts)
                                    └── TargetFunctions
                                          ├── CryticTester   + CryticAsserts  (Echidna/Medusa)
                                          └── CryticToFoundry + FoundryAsserts (Foundry/Halmos)
```

## Conventions

- Import `vm` from `@chimera/Hevm.sol` — NOT from forge-std
- Only use HEVM cheatcodes — Foundry-specific cheatcodes break Echidna/Medusa
- `startPrank`/`stopPrank` are safe in Foundry and Medusa, but NOT Echidna
- `etch` is safe in Medusa and Foundry, but NOT Echidna
- Property functions use `invariant_` prefix (works for both Echidna and Medusa)
- Import targets in alphabetical order in `TargetFunctions.sol`
- Apply `updateGhosts` to every handler that tests a transition invariant
- Always use `try/catch` in handlers — list expected reverts; `t(false, "unexpected")` on unknown
- Use `between()` for clamping, `precondition()` for state guards — never raw `require` in handlers
- `_getActor()` returns the currently active actor — use it instead of hardcoded addresses

## assert Backends

| Context | Backend | Use `between()` as |
|---------|---------|-------------------|
| Echidna/Medusa | CryticAsserts | modular clamp |
| Foundry | FoundryAsserts | modular clamp |
| Halmos | FoundryAsserts* | modular clamp (use `vm.assume` directly for symbolic bounds) |

## Reference

Full framework reference: `codex/resources/chimera-reference.md`
Config templates: `codex/resources/chimera-templates.md`
