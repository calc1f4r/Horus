---
# Core Classification
protocol: hydradx
chain: polkadot
category: oracle
vulnerability_type: price_manipulation
root_cause_family: stale_or_unsynced_state

# Pattern Identity
pattern_key: bypassed-oracle-update-path | EMA price oracle | direct transfer to AMM pool | price moves without oracle tracking

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - HydraDX Omnipool
  - EMA oracle feed
path_keys:
  - bypassed-oracle-update-path | direct transfer to Omnipool | pool reserves change without oracle hook | oracle price divergence
  - bypassed-oracle-update-path | reciprocal EMA | 1/ema(p) != ema(1/p) | TWAP inversion error
  - bypassed-oracle-update-path | MAX_UNIQUE_ENTRIES | dead configuration constant | missing aggregation bound

# Attack Vector Details
attack_type: data_manipulation
affected_component: price_feed (EMA oracle over Omnipool reserves)

# Oracle-Specific Fields
oracle_provider: custom
oracle_attack_vector: manipulation

# Technical Primitives
primitives:
  - ema_price
  - twap
  - omnipool_reserves
  - lazy_oracle_update
  - reciprocal_inversion
  - MAX_UNIQUE_ENTRIES
  - oracle_update_hook

# Grep / Hunt-Card Seeds
code_keywords:
  - ema
  - price
  - oracle
  - MAX_UNIQUE_ENTRIES
  - hub_asset
  - reserve
  - update_price
  - Omnipool

severity: medium
impact: incorrect_pricing
language: rust
tags:
  - substrate
  - oracle
  - hydradx
  - omnipool
  - ema
  - twap
  - price_manipulation
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [rvA1] | reports/substrate-l1_findings/hydradx-rv-ema-oracle-2023.md | MEDIUM | Runtime Verification | A1 lazy oracle update — direct transfers to Omnipool change price without oracle hooks (fixed by blocking direct transfers) |
| [rvA2] | reports/substrate-l1_findings/hydradx-rv-ema-oracle-2023.md | MEDIUM | Runtime Verification | A2 `1/ema(p) != ema(1/p)` — reciprocal of EMA is not EMA of the reciprocal (acknowledged) |
| [rvB1] | reports/substrate-l1_findings/hydradx-rv-ema-oracle-2023.md | LOW/INFO | Runtime Verification | B1 `MAX_UNIQUE_ENTRIES` defined but never used — aggregation bound not enforced |
| [x1] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-01] Users can MAKE EMA-Oracle price outdated with direct transfers to StableSwap |
| [x2] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-07] Re-adding assets to the omnipool can cause a problem with the oracle |
| [x3] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-09] Missing hook call will lead to incorrect oracle results |
| [x4] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-10] A huge loss of funds for all the users who try to remove liquidity after swapping got disabled at manipulated price. |
| [x5] | reports/substrate-l1_findings/composable-audits-halborn-audit20210229-pallets-core-pdf.md | CRITICAL | Halborn | 3.2 (HAL-02) ORACLE SLASHING MECHANISM BYPASS - CRITICAL Description: The Oracle pallet is responsible for calculating prices for an asset i |
| [x6] | reports/substrate-l1_findings/composable-halborn-core.md | CRITICAL | Halborn | 3.2 (HAL-02) ORACLE SLASHING MECHANISM BYPASS - CRITICAL Description: The Oracle pallet is responsible for calculating prices for an asset i |
| [x7] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Unauthorized price oracle conﬁgurations |

## Lazy EMA Oracle Diverges from Omnipool Spot Price via Un-Hooked Reserve Changes

**HydraDX's EMA oracle is updated through trade hooks, so direct token transfers into the Omnipool move reserves (and the real price) without moving the oracle — and inverting the EMA is not the EMA of the inverted price series** - representative of AMM-fed oracles whose update path can be bypassed by non-trade state changes.

### Overview

Runtime Verification's 2023 review of HydraDX's EMA oracle found: A1 (Medium, fixed) direct transfers to the Omnipool account change reserves with no oracle update hook, so the oracle tracks a stale price; A2 (Medium, acknowledged) consumers inverting the EMA get a systematically different series than the EMA computed in the inverted direction; B1 `MAX_UNIQUE_ENTRIES` is declared but unused.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the oracle only updates on trade execution, while pool reserves are also mutable by plain transfers, and because EMA — unlike a plain spot ratio — does not commute with reciprocal inversion."
- Pattern key: `bypassed-oracle-update-path | EMA price oracle | direct transfer to AMM pool | price moves without oracle tracking`
- Interaction scope: `multi_contract`
- Primary affected component(s): `EMA oracle update logic, Omnipool reserve accounting, oracle consumers (liquidations, minting)`
- Contracts / modules involved: `HydraDX Omnipool, EMA oracle feed`
- Path keys: `direct transfer to Omnipool`, `reciprocal EMA divergence`, `MAX_UNIQUE_ENTRIES unused`
- High-signal code keywords: `ema, oracle, MAX_UNIQUE_ENTRIES, update_price, hub_asset, reserve`
- Typical sink / impact: `stale/incorrect oracle price fed to consumers → mispriced liquidations or minting`
- Validation strength: `strong` (auditor-confirmed; A1 fixed by blocking direct transfers, A2 acknowledged by protocol)

#### Contract / Boundary Map

- Entry surface(s): plain token `transfer` to the Omnipool account; any swap on the pool; oracle read APIs used by consumers
- Contract hop(s): `tokens pallet transfer -> Omnipool reserves (no oracle call)` vs `swap -> update_price -> EMA storage`
- Trust boundary crossed: `oracle boundary — reserve state mutates across a path the oracle does not observe`
- Shared state or sync assumption: `EMA storage must reflect all state transitions that change the pool price, and consumers must use the EMA in the direction it was computed`

#### Valid Bug Signals

- Signal 1: The pool account accepts direct transfers (is not greedily rejecting non-pallet balance changes) and the oracle update lives only in the swap path ([rvA1]).
- Signal 2: An oracle consumer computes `1/ema(p)` (or converts between directions) instead of consuming a natively-computed inverse series ([rvA2]).
- Signal 3: A constant like `MAX_UNIQUE_ENTRIES` guarding oracle aggregation is declared but never referenced ([rvB1]).

#### False Positive Guards

- Not this bug when: the pool account rejects direct transfers (post-fix HydraDX behavior) or the oracle recomputes from absolute reserves on every read rather than incrementally on trades.
- Safe if: consumers only ever use the EMA in its computed direction and never invert it.
- Requires attacker control of: token balances sent directly to the pool account (Path A) — ordinary user capability pre-fix.

### Vulnerability Description

#### Root Cause

The EMA oracle is lazily updated inside trade execution, but the Omnipool's reserves can also change via direct transfers to the pool account (e.g., donations, mistakes, or deliberate manipulation), which skip the hook entirely ([rvA1]). Additionally, because EMA is a non-linear filter, the reciprocal of an EMA of prices is not equal to the EMA of reciprocal prices — consumers that invert introduce systematic divergence ([rvA2]). Finally, `MAX_UNIQUE_ENTRIES`, intended to bound the aggregation set, was never wired in ([rvB1]).

#### Attack Scenario / Path Variants

**Path A: Move real price without moving the oracle**
Path key: `bypassed-oracle-update-path | direct transfer to Omnipool | pool reserves change without oracle hook | oracle price divergence`
Entry surface: plain `transfer` to the Omnipool account
Contracts touched: `tokens pallet -> Omnipool reserves` (oracle untouched)
Boundary crossed: oracle update path
1. Attacker transfers a large quantity of an asset directly to the Omnipool account.
2. Reserves (and therefore any reserve-derived price) shift; the EMA oracle does not run — no trade occurred.
3. Consumers acting on the stale EMA (or on reserve-derived spot) misprice trades/liquidations in the attacker's favor window.

**Path B: Reciprocal inversion divergence**
Path key: `bypassed-oracle-update-path | reciprocal EMA | 1/ema(p) != ema(1/p) | TWAP inversion error`
Entry surface: oracle consumer reading the EMA for asset X priced in Y, but needing Y priced in X
1. Consumer reads `ema(p)` where p = X/Y and computes `1/ema(p)` for Y/X.
2. Because smoothing is non-linear, this differs from the true EMA of the Y/X series, especially in volatile windows.
3. Systematic pricing error accumulates in the consumer's logic.

**Path C: Unbounded aggregation set (dead constant)**
Path key: `bypassed-oracle-update-path | MAX_UNIQUE_ENTRIES | dead configuration constant | missing aggregation bound`
1. `MAX_UNIQUE_ENTRIES` exists in configuration but is never enforced.
2. The aggregation/history structure can grow or admit more entries than designed.
3. Weight/memory assumptions of the oracle break.

#### Vulnerable Pattern Examples

**Example 1: Oracle update only in the swap path (from [rvA1])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: reserves mutable by transfers; EMA updated only on trades
pub fn swap(origin: OriginFor<T>, asset_in: AssetId, asset_out: AssetId, amount: Amount) -> DispatchResult {
    // ... swap logic mutates reserves ...
    T::Oracle::update_price(&pair, new_price); // hook ONLY here
    Ok(())
}
// plain transfer to the pool account changes reserves with NO oracle update:
// balances.transfer(pool_account, 1_000_000 * UNIT) -> price shifted, EMA stale
```

**Example 2: Consumer inverts the EMA (from [rvA2])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: 1/ema(p) is NOT ema(1/p)
let price_x_per_y = Oracle::ema(X, Y);          // EMA of X/Y series
let price_y_per_x = FixedU128::one() / price_x_per_y; // ≠ EMA of Y/X series
// systematic divergence vs a natively maintained inverse oracle
```

**Example 3: Dead aggregation bound (from [rvB1])** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: constant declared, never enforced
pub const MAX_UNIQUE_ENTRIES: u32 = 100; // defined in oracle config
// ...nowhere in the codebase: ensure!(entries.len() <= MAX_UNIQUE_ENTRIES)
```

### Impact Analysis

#### Technical Impact

- Oracle/spot-price divergence window during and after direct transfers ([rvA1]).
- Systematic inversion error for any consumer needing the reverse-direction price ([rvA2]).
- Unenforced aggregation bounds erode weight and memory assumptions ([rvB1]).

#### Business Impact

- Oracles feeding liquidation/minting logic on stale or wrongly-inverted prices cause value extraction (unfair liquidations, over/under-collateralized mints) — Medium severity per RV.

#### Affected Scenarios

- Any AMM-reserve-derived oracle that updates only on trades while the pool account accepts direct transfers.
- Consumers needing bidirectional prices from a single-direction EMA.
- Oracle configs with declared-but-unwired bounds.

### Secure Implementation

**Fix 1: Make the pool account reject non-pallet transfers (applied fix for A1)**
```rust
// ✅ SECURE: reserves only mutable via pallet logic that always updates the oracle
impl fungibles::Mutate<_> for OmnipoolAsset {
    // block direct transfers into the pool account
}
// or: hold reserves in a dedicated account whose TransferOrigin rejects external senders,
// guaranteeing every reserve change passes through swap() -> update_price()
```

**Fix 2: Maintain native directional EMAs and enforce bounds**
```rust
// ✅ SECURE: compute each direction independently; wire in the bound
T::Oracle::update_price(X, Y, observed_xy); // EMA of X/Y
T::Oracle::update_price(Y, X, observed_yx); // separate EMA of Y/X (never invert)
ensure!(history.len() <= T::MaxUniqueEntries::get(), Error::TooManyEntries); // B1 fix
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- ema
- update_price
- MAX_UNIQUE_ENTRIES
- hub_asset
- oracle
- Omnipool
- reserve
```

#### Code Patterns to Look For
```
- Pattern 1: pool/AMM accounts that accept direct token transfers while oracle updates live only in swap functions
- Pattern 2: `1/ema(...)` or `FixedU128::one() / ema` at oracle consumption sites
- Pattern 3: oracle configuration constants with zero call sites
```

#### Audit Checklist
- [ ] List every code path that mutates pool reserves — does each trigger the oracle update?
- [ ] Does any consumer invert the oracle output instead of reading the reverse pair?
- [ ] Are declared oracle bounds (entry counts, history sizes) actually enforced at runtime?

### Keywords for Search

`EMA oracle`, `TWAP manipulation`, `lazy oracle update`, `HydraDX`, `Omnipool`, `oracle bypass`, `direct transfer manipulation`, `price divergence`, `reciprocal EMA`, `oracle inversion`, `MAX_UNIQUE_ENTRIES`, `AMM reserve oracle`, `stale price`, `Runtime Verification`, `price feed manipulation`, `substrate oracle`

### Related Vulnerabilities

- DB/substrate/amm/omnipool-liquidity-math.md (same Omnipool, liquidity math)
- DB/substrate/pallets/xcm-instruction-validation.md (XCM fee/waiver findings context)
