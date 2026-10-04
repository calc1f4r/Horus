---
# Core Classification
protocol: plume
chain: plume
category: accounting
vulnerability_type: snapshotless_batched_distribution

# Pattern Identity
root_cause_family: missing_snapshot
pattern_key: missing_balance_snapshot | batched_yield_distribution | inter_batch_transfer | double_yield_claim

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - ArcToken (distributeYield, distributeYieldWithLimit, _isYieldAllowed, holders set)
  - ArcTokenPurchase (stored ArcTokens / yield accrual)
  - ERC20 transfer logic (holders set add/remove + index swap)
path_keys:
  - missing_balance_snapshot | distributeYieldWithLimit | inter-batch transfer | double yield
  - holder_set_index_swap | distributeYieldWithLimit | EnumerableSet remove/append | omission + double-pay
  - division_remainder | distributeYieldWithLimit | last-batch remainder | permanently locked funds

# Attack Vector Details
attack_type: economic_exploit
affected_component: batched_yield_distribution

# Technical Primitives
primitives:
  - EnumerableSet holders array with swap-and-pop removal
  - live balanceOf reads per batch
  - effectiveTotalSupply recomputed per batch
  - startIndex/limit batch cursor
  - integer division remainder handling
  - ERC20Snapshot (absent)

# Grep / Hunt-Card Seeds
code_keywords:
  - distributeYieldWithLimit
  - distributeYield
  - effectiveTotalSupply
  - startIndex
  - lastProcessedIndex
  - _isYieldAllowed
  - holders
  - balanceOf

# Impact Classification
severity: high
impact: theft_of_unclaimed_yield_and_fund_freeze
exploitability: 0.8
financial_impact: high

# Context Tags
tags:
  - l1
  - rwa
  - arc-token
  - yield-distribution
  - solidity
  - batching
  - snapshot

# Version Info
language: solidity
version: "Plume Network Attackathon (immunefi-team/attackathon-plume-network), arc/src/ArcToken.sol, Jul-Aug 2025"
---

## References & Source Reports

> All paths verified to exist under `reports/plume-l1_findings/`. Second-largest high-severity cluster in the corpus (~30 near-duplicate highs against `arc/src/ArcToken.sol`).

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [PA1] | reports/plume-l1_findings/49710-sc-high-cross-batch-state-manipulation-in-yield-distribution-allows-double-dipping-of-yield-fu.md | HIGH | Immunefi (Attackathon) | Report #49710, ArcToken.sol |
| [PA2] | reports/plume-l1_findings/52371-sc-high-distributeyieldwithlimit-is-vulnerable-to-inter-batch-balance-and-holders-array-mutati.md | HIGH | Immunefi | Report #52371, ArcToken.sol |
| [PA3] | reports/plume-l1_findings/51558-sc-high-arctoken-holder-can-receive-yield-twice-from-distributeyieldwithlimit.md | HIGH | Immunefi | Report #51558, ArcToken.sol |
| [PA4] | reports/plume-l1_findings/52798-sc-high-integer-division-remainder-loss-in-batched-yield-distribution-causes-permanent-fund-lo.md | HIGH | Immunefi | Report #52798, ArcToken.sol (permanent freezing of funds) |

## Plume ArcToken Batched Yield Distribution Without Snapshots

### Overview

ArcToken — Plume's RWA yield-bearing token factory — distributes real-world-asset yield to holders via `distributeYieldWithLimit(...)`, which walks a **mutable** holders set in batches while reading **live** `balanceOf` values and recomputing `effectiveTotalSupply` per batch. Because no distribution-epoch snapshot of balances or of the holder list exists, any holder can move tokens between addresses/batches so the same tokens are paid in multiple batches, honest holders can be omitted via swap-and-pop index reordering, and per-batch division remainders are stranded in the contract with no recovery function. This single design flaw generated ~30 high-severity attackathon reports (theft of unclaimed yield / permanent fund freeze).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because batched yield distribution iterates a mutable holder set using live balances and per-batch denominators with no epoch snapshot, no claim-once tracking, and no remainder sweep — so inter-batch transfers change both numerator and index positions between batches."
- Pattern key: `missing_balance_snapshot | batched_yield_distribution | inter_batch_transfer | double_yield_claim`
- Interaction scope: `multi_contract` (ArcToken distribution ↔ ERC20 transfer hooks ↔ ArcTokenPurchase stored tokens)
- Primary affected component(s): `ArcToken.distributeYieldWithLimit, holders EnumerableSet, batch cursor state`
- Contracts / modules involved: `ArcToken, ArcTokenPurchase, holders set maintenance (transfer hooks)`
- Path keys: `missing_balance_snapshot | distributeYieldWithLimit | inter-batch transfer | double yield` · `holder_set_index_swap | distributeYieldWithLimit | EnumerableSet remove/append | omission + double-pay` · `division_remainder | distributeYieldWithLimit | last-batch remainder | permanently locked funds`
- High-signal code keywords: `distributeYieldWithLimit, effectiveTotalSupply, startIndex, lastProcessedIndex, _isYieldAllowed, holders, balanceOf`
- Typical sink / impact: `theft of yield intended for other holders; omitted holders; rounding remainders permanently locked`
- Validation strength: `strong` (#49710, #52371, #51558, #52798 read with code excerpts, PoC steps, and loss formulas)

#### Contract / Boundary Map

- Entry surface(s): `distributeYieldWithLimit(uint256 totalAmount, uint256 startIndex, uint256 limit)`, `distributeYield(...)`, any ERC20 `transfer()` between batches
- Contract hop(s): `distributor (EOA/agent) -> ArcToken.distributeYieldWithLimit -> balanceOf(holder) live reads -> transfer of yield out`
- Trust boundary crossed: `public token transfers mutate the iteration domain (holders set + balances) that the distributor assumes is frozen across batches`
- Shared state or sync assumption: `batch cursor (startIndex/limit) and holders-set indices must map to the same population/balances in every batch of one epoch — violated by construction`

#### Valid Bug Signals

- Signal 1: Per-holder share computed from `balanceOf(holder)` at batch time and a denominator (`effectiveTotalSupply`) recomputed per batch — no epoch snapshot (#49710 code excerpt verified).
- Signal 2: Holder removal swap-and-pops the last element into the removed index, so previously covered index ranges no longer map to the same addresses (#52371 "attack path 1" verified step-by-step).
- Signal 3: `distributeYield()` (unbatched) handles the final remainder correctly while `distributeYieldWithLimit()` drops it — inconsistent siblings in the same contract (#52798).
- Signal 4: Loss scales with batch count — "maximum theoretical loss ≈ (batches - 1) * attacker_token_balance * yield_per_token" (#49710 impact model).

#### False Positive Guards

- Not this bug when: balances and holder list are snapshotted (ERC20Snapshot-style) at epoch start and shares computed against the frozen snapshot.
- Not this bug when: the distribution is atomic (single `distributeYield()` pass) — no inter-batch window exists.
- Safe if: each address's epoch payment is tracked (claim-once map) and remainder is swept to the last holder / a designated sink.
- Requires attacker control of: only their own token movements between batches (fully permissionless); timing of batches is distributor/admin-controlled but multi-batch is the normal operating mode for large holder counts.
- Dust-only guard does NOT apply: loss scales with attacker balance and batch count, not with remainder dust.

### Vulnerability Description

#### Root Cause

Three conjoined flaws in `distributeYieldWithLimit` (per #49710 "three main design flaws"):
1. **Real-time balance checks** — "balances are read live during each batch processing (`balanceOf(holder)`)".
2. **No claim tracking** — "no storage of which addresses/tokens have received yield for the current distribution".
3. **Global amount over mutable denominator** — "a fixed `totalAmount` is divided across a mutable effective total supply computed from live balances".
Plus: **mutable iteration domain** — the holders set is an array-backed EnumerableSet where zero-balance removal swaps the last element into the hole and re-entrants append to the end (#52371, #51558), and **remainder mishandling** — per-batch division remainders accumulate with no sweep (#52798: "integer division remainders from each batch are permanently lost and locked in the contract... no recovery method available").

#### Attack Scenario / Path Variants

**Path A: Cross-batch double dipping**
Path key: `missing_balance_snapshot | distributeYieldWithLimit | inter-batch transfer | double yield`
Entry surface: `transfer()` between batch 1 and batch 2
Contracts touched: `ArcToken (distribution + transfer)`
Boundary crossed: `public transfer mutates distribution denominator/numerators mid-epoch`
1. Distribution runs in ≥2 batches (large holder set). Attacker holds tokens mapped to a batch-1 index and a fresh address with no history.
2. Attacker is paid in batch 1, then transfers the entire balance to the second address whose index falls in a later batch.
3. Batch 2 recomputes `effectiveTotalSupply` and pays the second address for the same underlying tokens.
4. Repeat per extra batch; honest holders' pro-rata share shrinks — theft of unclaimed yield.

**Path B: Index-swap omission + re-append double pay**
Path key: `holder_set_index_swap | distributeYieldWithLimit | EnumerableSet remove/append | omission + double-pay`
Entry surface: zero-out + refill of a holder balance between batches
1. Batch 1 pays attacker at index 6 (verified PoC geometry from #52371: 100 holders, batch = indices 1..50).
2. Attacker moves all ARC out — removal swap-pops the last holder into index 6; attacker's new address is appended (~index 98).
3. Batch 2 (indices 51..100) pays the attacker's new address again, while the swapped-in holder at index 6 is silently omitted for the epoch.
4. Both double-payment AND omission of a victim in one action.

**Path C: Remainder lock**
Path key: `division_remainder | distributeYieldWithLimit | last-batch remainder | permanently locked funds`
Entry surface: normal batched operation, no attacker needed
1. Each batch computes `share = (totalAmount * holderBalance) / effectiveTotalSupply`; remainders < 1 wei per holder per batch are dropped.
2. Aggregated across batches/epochs the dust is stranded; there is no sweep and `distributeYield()`'s correct last-holder handling is not replicated.
3. Yield tokens accumulate in the contract permanently (impact class: "Permanent freezing of funds", #52798/#53077/#52285/#52439).

#### Vulnerable Pattern Examples

**Example 1: Live balances, per-batch denominator** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: #49710 — ArcToken.sol distributeYieldWithLimit core
uint256 effectiveTotalSupply = 0;
for (uint256 i = 0; i < totalHolders; i++) {
    address holder = $.holders.at(i);
    if (_isYieldAllowed(holder)) {
        effectiveTotalSupply += balanceOf(holder); // ❌ live balance, changes between batches
    }
}
uint256 holderBalance = balanceOf(holder);                          // ❌ live again at pay time
uint256 share = (totalAmount * holderBalance) / effectiveTotalSupply; // ❌ floor remainder dropped
```

**Example 2: Mutable holder index across batch cursors** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: #52371/#51558 — batch cursor over an EnumerableSet that transfers mutate
function distributeYieldWithLimit(uint256 amount, uint256 startIndex, uint256 limit) external {
    for (uint256 i = startIndex; i < startIndex + limit; i++) {
        address holder = $.holders.at(i);   // ❌ index 6 now holds a DIFFERENT address after
        _payYield(holder, amount);          //    someone zeroed out (swap-and-pop); the emptied
    }                                       //    holder re-appended at the tail gets paid twice
}
```

**Example 3: Sibling functions disagree on remainder handling** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: #52798 — distributeYield() credits the final remainder, the batched variant doesn't
function distributeYield() internal {
    // ...pays all holders except last, then the LAST holder receives amount - paidSoFar; ✅ remainder kept
}
function distributeYieldWithLimit(uint256 amount, uint256 start, uint256 limit) internal {
    // ...pays [start, start+limit) with floor division, discards remainder ❌
    // no recoverYieldRemainder() exists anywhere in the contract ❌
}
```

### Impact Analysis

#### Technical Impact
- Same underlying tokens paid in multiple batches (double counting) while other holders are omitted entirely
- Distribution totals diverge from `totalAmount`; yield token inventory leaks/strands
- Permanent dust lock with no recovery entry point

#### Business Impact
- "Theft of unclaimed yield" (primary Immunefi impact across ~30 reports) directly undermines the RWA yield promise that ArcToken sells to tokenized-asset buyers
- Predictable, permissionless extraction devalues legitimate holders' APY; broken proportional accounting is an insolvency vector for the distributor

#### Affected Scenarios
- Any ArcToken with more holders than one batch limit (the intended production mode)
- Yield-restricted holders (`_isYieldAllowed` false) interacting with eligibility edges (#50252, #52572)
- ArcTokenPurchase stored-token accrual on top of batched distribution (#53001, #53016)

### Secure Implementation

**Fix 1: Snapshot the epoch — freeze population and balances once, pay against the snapshot, sweep remainders**
```solidity
// ✅ SECURE: distribution-epoch snapshot + claim-once + remainder sweep
struct Epoch { uint256 id; uint256 totalAmount; uint256 paidOut; uint256 snapshotId; mapping(address => bool) paid; }
function startYieldEpoch(uint256 totalAmount) external onlyRole(YIELD_DISTRIBUTOR) {
    uint256 snap = _snapshot();                 // ✅ ERC20Snapshot: freezes balances AND holder list
    epoch.totalAmount = totalAmount; epoch.snapshotId = snap; epoch.paidOut = 0;
}
function distributeYieldWithLimit(uint256 startIndex, uint256 limit) external onlyRole(YIELD_DISTRIBUTOR) {
    for (uint256 i = startIndex; i < startIndex + limit && i < holdersAtSnapshot(epoch.snapshotId).length; i++) {
        address holder = holderAtSnapshot(epoch.snapshotId, i);
        if (epoch.paid[holder] || !isYieldAllowedAt(epoch.snapshotId, holder)) continue; // ✅ claim-once
        uint256 bal = balanceOfAt(holder, epoch.snapshotId);        // ✅ frozen balance, not live
        uint256 share = (epoch.totalAmount * bal) / totalSupplyAt(epoch.snapshotId);
        epoch.paid[holder] = true;                                  // ✅ idempotent across batches
        epoch.paidOut += share;
        yieldToken.safeTransfer(holder, share);
    }
}
function endYieldEpoch() external onlyRole(YIELD_DISTRIBUTOR) {
    uint256 remainder = epoch.totalAmount - epoch.paidOut;
    if (remainder != 0) yieldToken.safeTransfer(REMAINDER_SINK, remainder); // ✅ nothing strands
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
distributeYieldWithLimit
distributeYield
effectiveTotalSupply
lastProcessedIndex
startIndex
_isYieldAllowed
balanceOfAt (absence-of signal: snapshot reads missing)
```

#### Code Patterns to Look For
```
- Batch loops reading balanceOf()/holders.at() instead of balanceOfAt()/snapshot arrays
- Any loop domain that public transfers can mutate (EnumerableSet/Array remove-swap-append)
- Denominator recomputed inside each batch instead of fixed at epoch start
- Floor-division payouts with no remainder sweep or sink at epoch close
- Two sibling distribution functions with different remainder semantics
```

#### Audit Checklist
- [ ] Are balances and the holder population frozen (snapshot) for the whole multi-batch epoch?
- [ ] Is each address's epoch payment idempotent (claim-once map) regardless of index churn?
- [ ] Is the denominator fixed at epoch start rather than recomputed per batch?
- [ ] Is every division remainder swept (last holder, sink, or carried to next epoch)?
- [ ] Do both batched and atomic distribution functions share identical accounting semantics?

### Real-World Examples

#### Known Exploits
- None public at time of writing; attackathon findings triaged via Immunefi.

#### Related CVEs/Reports
- Immunefi #49710, #52371, #51558, #52798 — Plume Network Attackathon 2025
- Near-duplicate family: #49787 (×2), #50527, #50507, #51414, #51658, #51754, #52198, #52254, #52347, #52517, #52634, #52680, #52845, #52956, #52961, #53077, #52285, #52439, #50735

### Prevention Guidelines

#### Development Best Practices
1. Never iterate a mutable set or read live balances across a multi-transaction distribution — snapshot first.
2. Track claim-once per (epoch, address) so index reordering cannot re-pay or omit.
3. Treat division remainders as liabilities: sweep them or carry them forward explicitly.

#### Testing Requirements
- Unit: zero-out/refill between batches (Path B geometry from #52371)
- Integration: 3-batch epoch with attacker spanning batches; assert total payouts == totalAmount
- Fuzz: random inter-batch transfers vs snapshot accounting; assert zero divergence

### Keywords for Search

`plume`, `arctoken`, `batched yield distribution`, `distributeYieldWithLimit`, `missing snapshot`, `balance snapshot`, `double dipping`, `double yield claim`, `inter-batch transfer`, `effectiveTotalSupply`, `EnumerableSet index swap`, `swap and pop`, `holder omission`, `division remainder`, `dust lock`, `permanently frozen yield`, `RWA tokenization`, `real world asset yield`, `theft of unclaimed yield`, `attackathon`, `immunefi`

### Related Vulnerabilities

- DB/unique/l1-misc/plume/plume-validator-commission-checkpoint-accounting.md (companion Plume cluster)
- DB/unique/l1-misc/vechain/ (sibling L1 reward-accounting entries from same distillation program)
