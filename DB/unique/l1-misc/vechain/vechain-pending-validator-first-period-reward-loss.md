---
# Core Classification
protocol: vechain-stargate
chain: vechain
category: state_accounting
vulnerability_type: skipped_reward_period

# Pattern Identity
root_cause_family: incorrect_initialization
pattern_key: cursor_over_start_boundary | lastClaimedPeriod-init | delegation-to-pending-validator | first-period-reward-loss

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Stargate.sol (delegate() initialization of lastClaimedPeriod)
  - ProtocolStaker (getValidationPeriodDetails / completedPeriods; pending validator status)
path_keys:
  - cursor_over_start_boundary | delegate-to-pending-validator | Stargate->ProtocolStaker

# Attack Vector Details
attack_type: logical_error
affected_component: reward cursor initialization on delegation

# Technical Primitives
primitives:
  - lastClaimedPeriod_cursor
  - completedPeriods_snapshot
  - pending_validator_status
  - startPeriod_derivation
  - plus_one_off_by_one

# Grep / Hunt-Card Seeds
code_keywords:
  - lastClaimedPeriod
  - completedPeriods
  - getValidationPeriodDetails
  - delegate
  - startPeriod
  - nextClaimablePeriod
  - getDelegationPeriodDetails
  - DelegationStatus.PENDING
  - validatorStatus
  - claimRewards

# Impact Classification
severity: high
impact: loss_of_accrued_rewards
financial_impact: medium

# Context Tags
tags:
  - defi
  - staking
  - rewards
  - off_by_one
  - initialization
  - l1

# Version Info
language: solidity
version: hayabusa-stargate-release
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [HIGH-1] | reports/vechain-l1_findings/59657-sc-high-delegators-lose-first-reward-period-when-delegating-to-pending-validators.md | HIGH | immunefi (@danvinci_20) | #59657 |
| [HIGH-2] | reports/vechain-l1_findings/59866-sc-high-the-delegator-s-rewards-in-period-1-cannot-be-claimed.md | HIGH | immunefi | #59866 |

## Delegating to a Pending Validator Skips the First Reward Period

**`delegate()` sets `lastClaimedPeriod = completedPeriods + 1`, but a pending validator's delegation actually starts at `completedPeriods + 1` → `nextClaimablePeriod` lands on `completedPeriods + 2` → first active period's VTHO is unclaimable**

### Overview

When a user delegates to a validator still in the PENDING phase, Stargate initializes the reward cursor one period past the delegation's true start: the code assumes delegation begins the period *after* next, while ProtocolStaker activates the delegation at `completedPeriods + 1`. The first active period is skipped and its rewards are permanently lost to the delegator.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because `delegate()` writes `lastClaimedPeriod[_tokenId] = completedPeriods + 1` while claim math derives `nextClaimablePeriod = lastClaimedPeriod + 1 = completedPeriods + 2`, but a PENDING validator's delegation `startPeriod` is `completedPeriods + 1` — the cursor is initialized past the first eligible period."
- Pattern key: `cursor_over_start_boundary | lastClaimedPeriod-init | delegation-to-pending-validator | first-period-reward-loss`
- Interaction scope: `multi_contract` (Stargate reward cursor ↔ ProtocolStaker period semantics)
- Primary affected component(s): `delegate()` cursor initialization, `_claimableDelegationPeriods` start handling
- Contracts / modules involved: `Stargate.sol`, `ProtocolStaker`
- Path keys: `cursor_over_start_boundary | delegate-to-pending-validator | Stargate->ProtocolStaker`
- High-signal code keywords: `lastClaimedPeriod`, `completedPeriods`, `getValidationPeriodDetails`, `startPeriod`, `nextClaimablePeriod`, `delegate`
- Typical sink / impact: `silent loss of one period of VTHO rewards per delegation (theft of unclaimed yield class)`
- Validation strength: `strong` (integration PoC prints `startPeriod=1, lastClaimedPeriod=1, nextClaimablePeriod=2`)

#### Contract / Boundary Map

- Entry surface(s): `delegate(tokenId, validator)` (user), `claimRewards(tokenId)` (user)
- Contract hop(s): `Stargate.delegate -> ProtocolStaker.getValidationPeriodDetails(completedPeriods) -> lastClaimedPeriod write; later Stargate.claimRewards -> _claimableDelegationPeriods (starts at +2)`
- Trust boundary crossed: reward cursor assuming ACTIVE-validator timing while ProtocolStaker applies PENDING-validator timing
- Shared state or sync assumption: delegation `startPeriod` (ProtocolStaker) must equal the first period the Stargate cursor will pay

#### Valid Bug Signals

- Signal 1: validator status PENDING at `delegate()` time; delegation's `startPeriod == completedPeriods + 1`
- Signal 2: after the validator activates, `getLastClaimedPeriod(tokenId) == startPeriod` and thus `nextClaimablePeriod == startPeriod + 1` — period `startPeriod` never claimable
- Signal 3: observed PoC output `start period: 1n / lastClaimedPeriod: 1n / nextClaimablePeriod: 2n`

#### False Positive Guards

- Not this bug when: delegating to an already-ACTIVE validator whose delegation truly starts at `completedPeriods + 2` (cursor matches start)
- Not this bug when: `_claimableDelegationPeriods` clamps `nextClaimablePeriod` down to `startPeriod` (it only clamps *up*: `if (next < startPeriod) next = startPeriod`)
- Safe if: initialization writes `lastClaimedPeriod = completedPeriods` for pending validators, or claim math uses `max(startPeriod, lastClaimedPeriod)` semantics that include the first active period
- Impact ceiling: one period of rewards per delegation event — loss, not freeze/theft of principal

### Vulnerability Description

#### Root Cause

`delegate()` snapshots the validator's completed periods and advances the cursor by one, encoding the assumption "delegation becomes active one period after delegation." For PENDING validators, ProtocolStaker actually activates the delegation at `completedPeriods + 1`. Since rewards begin at `nextClaimablePeriod = lastClaimedPeriod + 1`, the first active period (`completedPeriods + 1`) is skipped: rewards for it accrue to the pool but are unclaimable by the delegator.

#### Attack Scenario / Path Variants

**Path A: Delegate to newly-added (PENDING) validator**
Path key: `cursor_over_start_boundary | delegate-to-pending-validator | Stargate->ProtocolStaker`
1. New validator calls `addValidation` — status PENDING.
2. User stakes, NFT matures, calls `delegate(tokenId, newValidator)`.
3. `lastClaimedPeriod[tokenId] = completedPeriods + 1`; delegation `startPeriod = completedPeriods + 1`.
4. Validator activates; period `startPeriod` completes with the user's stake effective.
5. `claimRewards` starts at `startPeriod + 1` — first period's VTHO silently lost.

**Path B: Redelegation variants**
Path key: `cursor_over_start_boundary | delegate-to-pending-validator | Stargate->ProtocolStaker`
1. Same mis-initialization applies on any re-delegate targeting a pending validator, multiplying per-user losses.

#### Vulnerable Pattern Examples

**Example 1: Cursor initialization in delegate() (Stargate.sol)** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: assumes next-period activation for ALL validator states
(, , , uint32 completedPeriods) = $.protocolStakerContract.getValidationPeriodDetails(_validator);
$.lastClaimedPeriod[_tokenId] = completedPeriods + 1; // current period
// For PENDING validators the delegation actually starts AT completedPeriods + 1,
// so this write marks the first payable period as already claimed.
```

**Example 2: Claim math adds another +1**
```solidity
// ❌ VULNERABLE: the skipped period falls out of the arithmetic
uint32 nextClaimablePeriod = $.lastClaimedPeriod[_tokenId] + 1; // == completedPeriods + 2
if (nextClaimablePeriod < startPeriod) {
    nextClaimablePeriod = startPeriod; // clamp-up never rescues period startPeriod
}
```

**Example 3: PoC-observed state (integration test output)**
```solidity
// ❌ VULNERABLE: observed on vechain_solo:
// start period of delegation: 1n        (ProtocolStaker)
// newValidatorStatus: 1n                (PENDING)
// lastClaimedPeriod: 1n                 (Stargate cursor)
// nextClaimablePeriod: 2n               -> period 1 rewards unreachable
```

### Impact Analysis

#### Technical Impact
- First active period's rewards stranded in the reward pool for every delegation to a pending validator
- Systematic under-payment; no state corruption (pure loss, not freeze)

#### Business Impact
- Recurring per-user yield loss; predictable user complaints at every new-validator onboarding wave

#### Affected Scenarios
- New validators joining (always PENDING first) — the common growth path
- Compounds with post-exit over-claim bug: both ends of the cursor lifecycle mishandle boundaries

### Secure Implementation

**Fix 1: Status-aware cursor initialization**
```solidity
// ✅ SECURE: align the cursor with the actual activation period
(, , , uint32 completedPeriods) = $.protocolStakerContract.getValidationPeriodDetails(_validator);
(, , , , uint256 vStatus, ) = $.protocolStakerContract.getValidation(_validator);
if (vStatus == VALIDATOR_STATUS_PENDING) {
    $.lastClaimedPeriod[_tokenId] = completedPeriods;     // first active period stays claimable
} else {
    $.lastClaimedPeriod[_tokenId] = completedPeriods + 1; // active-validator timing unchanged
}
```

**Fix 2: Clamp-down in claim window**
```solidity
// ✅ SECURE: window may never start after the delegation's startPeriod
uint32 nextClaimablePeriod = $.lastClaimedPeriod[_tokenId] + 1;
if (nextClaimablePeriod < startPeriod) nextClaimablePeriod = startPeriod;
if ($.lastClaimedPeriod[_tokenId] < startPeriod) {
    nextClaimablePeriod = startPeriod; // repair already-skipped cursors
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Reward cursor initialized from a snapshot (+1) without consulting lifecycle status of the target
- Two sources of truth for "when does staking begin" (cursor vs delegation startPeriod) drifting apart
- View functions exposing startPeriod and lastClaimedPeriod that can be diffed on-chain
```

#### High-Signal Grep Seeds
```
- lastClaimedPeriod[
- completedPeriods + 1
- getValidationPeriodDetails
- startPeriod
- getDelegationPeriodDetails
- VALIDATOR_STATUS_PENDING
```

#### Code Patterns to Look For
```
- Pattern 1: `lastClaimedPeriod[x] = completedPeriods + 1` writes at delegation time
- Pattern 2: window functions that only clamp the lower bound upward
- Pattern 3: tests logging startPeriod vs lastClaimedPeriod equality (the smoking gun in the PoC)
```

#### Audit Checklist
- [ ] For each validator status (QUEUED/PENDING/ACTIVE/EXITING/EXITED), assert cursor ≤ startPeriod at delegation
- [ ] Property: first active period is always included in the first claim window
- [ ] Check redelegation path initializes the cursor identically correctly

### Real-World Examples

#### Known Exploits
- **VeChain Stargate (hayabusa audit comp)** — first reward period lost when delegating to pending validators — Nov 2025 — contest finding
  - Link: https://reports.immunefi.com/vechain-or-stargate-hayabusa (reports #59657, #59866)
  - Root cause: `lastClaimedPeriod = completedPeriods + 1` initialization vs `startPeriod = completedPeriods + 1` activation

#### Related CVEs/Reports
- Mirror-boundary bug: post-exit over-claim family (#59563 et al.) — same cursor, opposite boundary

### Prevention Guidelines

#### Development Best Practices
1. Derive the reward cursor from the delegation's canonical `startPeriod`, never from an independent +1 snapshot
2. Snapshot lifecycle status whenever period math depends on activation timing

#### Testing Requirements
- Unit: delegate while PENDING → fast-forward one period → claim must include that period
- Fuzz: invariant `firstClaimablePeriod == startPeriod` across all validator statuses

### Keywords for Search

`vechain`, `stargate`, `pending validator`, `lastClaimedPeriod`, `completedPeriods`, `startPeriod`, `nextClaimablePeriod`, `reward cursor`, `off-by-one`, `skipped period`, `first period loss`, `delegation`, `VTHO`, `reward initialization`, `validator status`, `claim window`, `underpayment`, `staking`, `off-by-one initialization`

### Related Vulnerabilities

- vechain-post-exit-delegation-reward-drain-off-by-one.md (upper boundary of same cursor)
- vechain-double-effective-stake-decrement-unstake-freeze.md (stake ledger during same lifecycle)
