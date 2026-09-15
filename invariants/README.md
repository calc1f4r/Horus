# Canonical Invariant Library

> Protocol-type-agnostic, language-agnostic invariant reference library.
> Mined from production DeFi protocols, standard specifications, formal verification specs,
> fuzzing property suites, and Horus.
>
> **Consumer**: `invariant-writer` agent uses these files as canonical seed context
> during Phase 0 (Protocol Research & Classification).

## Usage

When auditing a protocol of type X, load the relevant category files:

| Protocol Type | Load These Files |
|---------------|-----------------|
| Staking / LST / Restaking | `staking/*.md`, `universal/*.md` (when available) |
| Lending | `lending/*.md`, `universal/*.md`, `token/erc20.md` (when available) |
| DEX / AMM | `amm/*.md`, `universal/*.md`, `token/erc20.md` (when available) |
| Vault / Yield | `vault/*.md`, `universal/*.md`, `token/erc20.md` (when available) |
| Governance | `governance/*.md`, `universal/*.md` (when available) |
| Stablecoin | `stablecoin/*.md`, `lending/liquidation.md`, `universal/*.md` (when available) |
| Perpetuals | `perpetuals/*.md`, `universal/*.md`, `lending/liquidation.md` (when available) |
| Bridge | `bridge/*.md`, `universal/*.md` (when available) |

## Category Index

| Category | Files | Invariant Count | Top Sources |
|----------|-------|-----------------|-------------|
| staking | 8 files | 95 | EigenLayer, Lido, Cosmos SDK, GoGoPool, Aave, Morpho Blue |

### Staking Category Detail

| File | Invariant Count | Focus |
|------|-----------------|-------|
| [staking/exchange-rate.md](staking/exchange-rate.md) | 12 | LST/LRT exchange rate correctness, oracle integrity, sandwich resistance |
| [staking/withdrawal-queue.md](staking/withdrawal-queue.md) | 14 | Withdrawal queue conservation, fund accessibility, slippage protection |
| [staking/slashing.md](staking/slashing.md) | 12 | Slashing correctness, penalty distribution, protocol solvency |
| [staking/reward-distribution.md](staking/reward-distribution.md) | 11 | Reward distribution correctness, frontrunning resistance, accounting |
| [staking/share-accounting.md](staking/share-accounting.md) | 11 | Share/TVL accounting, first-depositor resistance, rounding rules |
| [staking/operator-delegation.md](staking/operator-delegation.md) | 10 | Operator management, delegation correctness, minipool security |
| [staking/beacon-chain-proofs.md](staking/beacon-chain-proofs.md) | 10 | Beacon chain proof verification, attestation, EigenPod accounting |
| [staking/general-staking.md](staking/general-staking.md) | 14 | Universal staking properties, lifecycle, conservation, fees |

**Total: 94 invariants across 8 files**

## How Invariants Are Sourced

1. **Formal verification specs** — formally verified properties from production protocols (Certora CVL, Sui Prover, etc.)
2. **Property tests** — fuzz-tested invariants (Echidna, Medusa, etc.)
3. **Stateful fuzz tests** — stateful fuzz-tested properties (Foundry invariant tests, etc.)
4. **Standard specifications** — mandatory standard behaviors (EIP, CW, SPL, etc.)
5. **Protocol documentation** — design-level constraints
6. **Horus** — inverted root causes of known exploits
7. **Web research** — academic papers, audit reports, blog posts

## Invariant Format

Each invariant entry contains:

| Field | Description |
|-------|-------------|
| **ID** | `CATEGORY-SUBCATEGORY-NNN` unique identifier |
| **Property (English)** | Plain English, precise, falsifiable statement |
| **Property (Formal)** | Mathematical predicate using standard notation |
| **Mode** | POSITIVE (must hold), NEGATIVE (must not happen), DUAL (both) |
| **Priority** | CRITICAL / HIGH / MEDIUM / LOW |
| **Multi-Call** | YES if exploitable through multi-transaction sequences |
| **Universality** | UNIVERSAL or CONDITIONAL (requires specific design pattern) |
| **Conditions** | When the invariant applies |
| **Source Evidence** | Protocol name, file path, tool used |
| **Why This Matters** | Impact of violation |
| **Known Violations** | Links to DB vulnerability patterns |
