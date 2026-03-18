<!-- AUTO-GENERATED from `.claude/rules/invariants.md`; source_sha256=1d1d79bd0620cde6005a8b8655ab4627d57caac3d4c53b828732099cb192b220 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/invariants.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "invariants/**/*.md"
---

# Invariant Library Rules

When creating or editing invariant files in `invariants/`:

## ID Format

Every invariant must use the canonical ID format: `CATEGORY-SUBCATEGORY-NNN`
- Examples: `STAKING-EXCHANGE-RATE-001`, `LENDING-LIQUIDATION-007`, `AMM-CONSERVATION-003`
- IDs must be unique within the library

## Required Fields Per Invariant Entry

Each invariant entry must include all of these:

| Field | Requirement |
|-------|-------------|
| **ID** | Unique `CATEGORY-SUBCATEGORY-NNN` identifier |
| **Property (English)** | Plain English, precise, falsifiable statement — no vague language |
| **Property (Formal)** | Mathematical predicate (∀, ∃, →, ≤, ≥, =) using standard notation |
| **Mode** | `POSITIVE` (must hold), `NEGATIVE` (must not happen), or `DUAL` (both) |
| **Priority** | `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` |
| **Multi-Call** | `YES` if exploitable through multi-transaction sequences, `NO` otherwise |
| **Universality** | `UNIVERSAL` or `CONDITIONAL` (with note on required design pattern) |
| **Conditions** | When the invariant applies (always, or specific state/configuration) |
| **Source Evidence** | Protocol name + file path + tool (e.g., "EigenLayer certora/specs/DelegationManager.spec") |
| **Why This Matters** | Concrete impact if violated (loss of funds, DoS, state corruption, etc.) |
| **Known Violations** | Links to DB patterns that represent violations of this invariant |

## Content Rules

- Properties must be **falsifiable** — if you can't write a test for it, restate it until you can
- Formal properties must use quantifiers correctly — `∀` for universal, `∃` for existential
- `POSITIVE` invariants describe what must always be true (conservation laws, ordering guarantees)
- `NEGATIVE` invariants describe what must never happen (fund loss, overflow, unauthorized access)
- `Multi-Call: YES` invariants require multi-step attack scenario description
- `UNIVERSAL` means the invariant applies to ALL protocols of this type; `CONDITIONAL` means it only applies when a specific mechanism is present
- Source Evidence must point to a real, verifiable source (not hypothetical)
- Known Violations should link to `DB/` entries by pattern ID (e.g., `oracle-staleness-001`)

## Category Directories

Match the protocol type to the correct subdirectory:
- `staking/` — LST, LRT, restaking, Cosmos/PoS staking
- `lending/` — money markets, collateralized lending, liquidation
- `amm/` — DEX, AMM, constant-product, concentrated liquidity
- `vault/` — ERC4626, yield strategies, share accounting
- `governance/` — DAO voting, timelocks, proposal systems
- `bridge/` — cross-chain messaging, lock-mint, proof validation
- `perpetuals/` — perps, funding rates, margin accounting

## After Adding Invariants

Update the `invariants/README.md` Category Index table with new file counts and invariant totals.
